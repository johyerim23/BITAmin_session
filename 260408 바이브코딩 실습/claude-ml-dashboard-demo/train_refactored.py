"""Refactored version of train.py.

Changes from original:
- Extracted load_data(), build_model(), run_cross_validation(),
  run_oof_evaluation(), run_test_evaluation(), and save_results()
  so each function has a single responsibility.
- train_and_evaluate() now orchestrates these helpers, making the
  high-level flow readable at a glance.
- No behaviour changes; results are identical to the original.
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_predict,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch

RANDOM_STATE = 42
RESULT_PATH = "results.json"
CV_N_JOBS = 1


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_data() -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    """Load the Wine dataset and return (X, y, target_names, feature_names)."""
    data: Bunch = load_wine()
    return (
        data.data,
        data.target,
        list(data.target_names),
        list(data.feature_names),
    )


def split_data(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Stratified train/test split."""
    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def build_model() -> Pipeline:
    """Return a StandardScaler + LogisticRegression pipeline."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ])


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def run_cross_validation(
    model: Pipeline,
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> dict[str, Any]:
    """Repeated stratified k-fold cross-validation on the training set."""
    cv = RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=5,
        random_state=RANDOM_STATE,
    )
    scores = cross_val_score(
        model, X_train, y_train,
        cv=cv,
        scoring="accuracy",
        n_jobs=CV_N_JOBS,
    )
    return {
        "strategy": "RepeatedStratifiedKFold",
        "n_splits": 5,
        "n_repeats": 5,
        "scoring": "accuracy",
        "scores": [float(s) for s in scores],
        "mean_accuracy": float(np.mean(scores)),
        "std_accuracy": float(np.std(scores)),
    }


def run_oof_evaluation(
    model: Pipeline,
    X_train: np.ndarray,
    y_train: np.ndarray,
    target_names: list[str],
) -> dict[str, Any]:
    """Out-of-fold predictions via StratifiedKFold."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    oof_pred = cross_val_predict(
        model, X_train, y_train,
        cv=cv,
        n_jobs=CV_N_JOBS,
    )
    report = classification_report(
        y_train, oof_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_train, oof_pred)
    return {
        "strategy": "StratifiedKFold",
        "n_splits": 5,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
    }


def run_test_evaluation(
    model: Pipeline,
    X_test: np.ndarray,
    y_test: np.ndarray,
    target_names: list[str],
) -> dict[str, Any]:
    """Evaluate the fitted model on the held-out test set."""
    y_pred = model.predict(X_test)
    report = classification_report(
        y_test, y_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_test, y_pred)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
    }


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_results(results: dict[str, Any], path: str = RESULT_PATH) -> None:
    """Serialise results to a JSON file."""
    Path(path).write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def train_and_evaluate() -> dict[str, Any]:
    """End-to-end training and evaluation pipeline."""
    X, y, target_names, feature_names = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = build_model()

    cv_results = run_cross_validation(model, X_train, y_train)
    oof_results = run_oof_evaluation(model, X_train, y_train, target_names)

    model.fit(X_train, y_train)
    test_results = run_test_evaluation(model, X_test, y_test, target_names)

    results: dict[str, Any] = {
        "dataset": "Wine",
        "model_name": "LogisticRegression + StandardScaler",
        "random_state": RANDOM_STATE,
        "n_samples_total": int(len(X)),
        "n_features": int(X.shape[1]),
        "feature_names": feature_names,
        "class_names": target_names,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "cross_validation": cv_results,
        "oof_evaluation": oof_results,
        "test_evaluation": test_results,
    }

    save_results(results)
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    results = train_and_evaluate()

    print("\n=== Model Summary ===")
    print("Dataset:", results["dataset"])
    print("Model:", results["model_name"])
    print("Train size:", results["train_size"])
    print("Test size:", results["test_size"])

    print("\n=== Cross Validation ===")
    cv = results["cross_validation"]
    print(f"CV Accuracy: {cv['mean_accuracy']:.4f} (± {cv['std_accuracy']:.4f})")

    print("\n=== Test Evaluation ===")
    print(f"Test Accuracy: {results['test_evaluation']['accuracy']:.4f}")

    print("\nresults.json 파일 저장 완료")
