import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import (
    train_test_split,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_score,
    cross_val_predict,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
RESULT_PATH = "results.json"
CV_N_JOBS = 1


def build_model():
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ])
    return model


def train_and_evaluate():
    # 1) 데이터 로드
    data = load_wine()
    X = data.data
    y = data.target
    target_names = list(data.target_names)
    feature_names = list(data.feature_names)

    # 2) train / test 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = build_model()

    # 3) 반복 교차검증: 평균 성능 확인용
    repeated_cv = RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=5,
        random_state=RANDOM_STATE,
    )

    cv_scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=repeated_cv,
        scoring="accuracy",
        n_jobs=CV_N_JOBS,
    )

    # 4) OOF 예측용: partition 보장되는 CV 사용
    oof_cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    oof_pred = cross_val_predict(
        model,
        X_train,
        y_train,
        cv=oof_cv,
        n_jobs=CV_N_JOBS,
    )

    oof_report = classification_report(
        y_train,
        oof_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )

    oof_confusion = confusion_matrix(y_train, oof_pred)

    # 5) 전체 train으로 학습 후 최종 test 평가
    model.fit(X_train, y_train)
    y_test_pred = model.predict(X_test)

    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_report = classification_report(
        y_test,
        y_test_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
    test_confusion = confusion_matrix(y_test, y_test_pred)

    results = {
        "dataset": "Wine",
        "model_name": "LogisticRegression + StandardScaler",
        "random_state": RANDOM_STATE,
        "n_samples_total": int(len(X)),
        "n_features": int(X.shape[1]),
        "feature_names": feature_names,
        "class_names": target_names,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "cross_validation": {
            "strategy": "RepeatedStratifiedKFold",
            "n_splits": 5,
            "n_repeats": 5,
            "scoring": "accuracy",
            "scores": [float(x) for x in cv_scores],
            "mean_accuracy": float(np.mean(cv_scores)),
            "std_accuracy": float(np.std(cv_scores)),
        },
        "oof_evaluation": {
            "strategy": "StratifiedKFold",
            "n_splits": 5,
            "classification_report": oof_report,
            "confusion_matrix": oof_confusion.tolist(),
        },
        "test_evaluation": {
            "accuracy": float(test_accuracy),
            "classification_report": test_report,
            "confusion_matrix": test_confusion.tolist(),
        },
    }

    Path(RESULT_PATH).write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return results


if __name__ == "__main__":
    results = train_and_evaluate()

    print("\n=== Model Summary ===")
    print("Dataset:", results["dataset"])
    print("Model:", results["model_name"])
    print("Train size:", results["train_size"])
    print("Test size:", results["test_size"])

    print("\n=== Cross Validation ===")
    print(
        f"CV Accuracy: {results['cross_validation']['mean_accuracy']:.4f} "
        f"(± {results['cross_validation']['std_accuracy']:.4f})"
    )

    print("\n=== Test Evaluation ===")
    print(f"Test Accuracy: {results['test_evaluation']['accuracy']:.4f}")

    print("\nresults.json 파일 저장 완료")