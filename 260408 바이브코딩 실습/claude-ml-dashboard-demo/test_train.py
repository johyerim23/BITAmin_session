"""pytest tests for train.py — verifies train_and_evaluate() behavior."""

import json
from pathlib import Path

import pytest

from train import train_and_evaluate, RESULT_PATH


@pytest.fixture(scope="module")
def results():
    """Run train_and_evaluate() once and share the result across tests."""
    return train_and_evaluate()


# ---------------------------------------------------------------------------
# Return-type checks
# ---------------------------------------------------------------------------

class TestReturnType:
    def test_returns_dict(self, results):
        assert isinstance(results, dict), "train_and_evaluate() must return a dict"


# ---------------------------------------------------------------------------
# Top-level key existence
# ---------------------------------------------------------------------------

class TestTopLevelKeys:
    REQUIRED_KEYS = [
        "dataset",
        "model_name",
        "random_state",
        "n_samples_total",
        "n_features",
        "feature_names",
        "class_names",
        "train_size",
        "test_size",
        "cross_validation",
        "oof_evaluation",
        "test_evaluation",
    ]

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_key_present(self, results, key):
        assert key in results, f"Missing top-level key: '{key}'"


# ---------------------------------------------------------------------------
# cross_validation section
# ---------------------------------------------------------------------------

class TestCrossValidation:
    REQUIRED_KEYS = ["strategy", "n_splits", "n_repeats", "scoring", "scores",
                     "mean_accuracy", "std_accuracy"]

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_key_present(self, results, key):
        assert key in results["cross_validation"], (
            f"Missing cross_validation key: '{key}'"
        )

    def test_mean_accuracy_in_range(self, results):
        acc = results["cross_validation"]["mean_accuracy"]
        assert 0.0 <= acc <= 1.0, f"mean_accuracy out of range: {acc}"

    def test_scores_all_in_range(self, results):
        scores = results["cross_validation"]["scores"]
        assert isinstance(scores, list) and len(scores) > 0
        for s in scores:
            assert 0.0 <= s <= 1.0, f"CV score out of range: {s}"

    def test_std_accuracy_non_negative(self, results):
        std = results["cross_validation"]["std_accuracy"]
        assert std >= 0.0, f"std_accuracy must be non-negative: {std}"


# ---------------------------------------------------------------------------
# oof_evaluation section
# ---------------------------------------------------------------------------

class TestOofEvaluation:
    REQUIRED_KEYS = ["strategy", "n_splits", "classification_report", "confusion_matrix"]

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_key_present(self, results, key):
        assert key in results["oof_evaluation"], (
            f"Missing oof_evaluation key: '{key}'"
        )

    def test_oof_accuracy_in_range(self, results):
        acc = results["oof_evaluation"]["classification_report"]["accuracy"]
        assert 0.0 <= acc <= 1.0, f"OOF accuracy out of range: {acc}"

    def test_confusion_matrix_is_list(self, results):
        cm = results["oof_evaluation"]["confusion_matrix"]
        assert isinstance(cm, list), "confusion_matrix must be a list"


# ---------------------------------------------------------------------------
# test_evaluation section
# ---------------------------------------------------------------------------

class TestTestEvaluation:
    REQUIRED_KEYS = ["accuracy", "classification_report", "confusion_matrix"]

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_key_present(self, results, key):
        assert key in results["test_evaluation"], (
            f"Missing test_evaluation key: '{key}'"
        )

    def test_accuracy_is_float(self, results):
        acc = results["test_evaluation"]["accuracy"]
        assert isinstance(acc, float), f"accuracy must be float, got {type(acc)}"

    def test_accuracy_in_range(self, results):
        acc = results["test_evaluation"]["accuracy"]
        assert 0.0 <= acc <= 1.0, f"test accuracy out of range: {acc}"

    def test_confusion_matrix_is_list(self, results):
        cm = results["test_evaluation"]["confusion_matrix"]
        assert isinstance(cm, list), "confusion_matrix must be a list"


# ---------------------------------------------------------------------------
# Dataset metadata
# ---------------------------------------------------------------------------

class TestDatasetMetadata:
    def test_dataset_name(self, results):
        assert results["dataset"] == "Wine"

    def test_n_samples_positive(self, results):
        assert results["n_samples_total"] > 0

    def test_n_features_positive(self, results):
        assert results["n_features"] > 0

    def test_train_test_split_sum(self, results):
        total = results["n_samples_total"]
        train = results["train_size"]
        test = results["test_size"]
        assert train + test == total, (
            f"train ({train}) + test ({test}) != total ({total})"
        )

    def test_feature_names_is_list(self, results):
        assert isinstance(results["feature_names"], list)
        assert len(results["feature_names"]) == results["n_features"]

    def test_class_names_is_list(self, results):
        assert isinstance(results["class_names"], list)
        assert len(results["class_names"]) > 0


# ---------------------------------------------------------------------------
# results.json file creation
# ---------------------------------------------------------------------------

class TestResultsJson:
    def test_file_created(self, results):
        path = Path(RESULT_PATH)
        assert path.exists(), f"results.json not found at {RESULT_PATH}"

    def test_file_is_valid_json(self, results):
        path = Path(RESULT_PATH)
        content = path.read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert isinstance(parsed, dict)

    def test_file_accuracy_matches_return_value(self, results):
        path = Path(RESULT_PATH)
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert parsed["test_evaluation"]["accuracy"] == results["test_evaluation"]["accuracy"]
