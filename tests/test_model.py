import json
from pathlib import Path

from app import PredictionRequest, predict

CFG = json.loads(Path("config.json").read_text())


def test_metrics_file():
    m = json.loads(Path("artifacts/metrics.json").read_text())
    assert m["student_id"] == CFG["student_id"]
    assert m["training_rows"] >= 100
    assert 0.5 < m["accuracy"] <= 1.0


def test_predict():
    rec = {f: 0.0 for f in CFG["features"]}
    out = predict(PredictionRequest(records=[rec]))
    assert len(out["predictions"]) == 1
    assert 0.0 <= out["probabilities"][0] <= 1.0
