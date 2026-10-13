"""Regression checks for audit security, CSV conversion, API and static console."""
import csv
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from agents.base import AuditTrail
from agents.api import app
from cli import main as main_cli, parse_csv_bool as main_bool
from protein_lm_agent.cli import main as frontier_cli, parse_csv_bool as frontier_bool

ROOT = Path(__file__).resolve().parent.parent


def test_hmac_detects_tampered_entries_and_protects_internal_state():
    audit = AuditTrail(secret_key="test-key-for-fixture")
    first = audit.log("worker", "test", "START", {"value": "safe"})
    audit.log("worker", "test", "END", {"value": "safe"})
    assert audit.verify_integrity()
    snapshot = audit.get_trail()
    snapshot[0]["actor"] = "untrusted"
    assert audit.verify_integrity()  # copying a snapshot cannot alter stored entries
    audit.logs[0]["actor"] = "tampered"
    assert not audit.verify_integrity()
    audit.logs[0]["actor"] = "worker"
    assert audit.verify_integrity()
    audit.logs[1]["current_hash"] = "0" * 64
    assert not audit.verify_integrity()


@pytest.mark.parametrize("parser", [main_bool, frontier_bool])
@pytest.mark.parametrize(("value", "expected"), [
    ("False", False), ("false", False), ("0", False), ("No", False),
    ("", False), (None, False), ("True", True), ("1", True), ("YES", True),
])
def test_csv_boolean_parsing(parser, value, expected):
    assert parser(value) is expected


@pytest.mark.parametrize("parser", [main_bool, frontier_bool])
def test_invalid_boolean_rejected(parser):
    with pytest.raises(ValueError, match="Invalid is_critical_flag"):
        parser("probably")


@pytest.mark.parametrize("main, status_field, expected", [
    (main_cli, "overall_urgency", "ROUTINE"),
    (frontier_cli, "overall_status", "NOMINAL_OPTIMAL"),
])
def test_batch_false_is_not_critical(tmp_path, main, status_field, expected):
    source = tmp_path / "input.csv"
    output = tmp_path / "result.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "T-1,TARGET-1,12,4,False,NOMINAL\n", encoding="utf-8"
    )
    assert main(["batch", "-i", str(source), "-o", str(output)]) == 0
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0][status_field] == expected


def test_api_errors_metrics_and_audit_log_access(monkeypatch):
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    monkeypatch.delenv("AUDIT_LOG_TOKEN", raising=False)
    assert client.get("/api/audit/logs").status_code == 503
    monkeypatch.setenv("AUDIT_LOG_TOKEN", "local-test-token")
    assert client.get("/api/audit/logs").status_code == 403
    assert client.get("/api/audit/logs", headers={"X-Audit-Token": "local-test-token"}).status_code == 200
    payload = {
        "task_id": "SMOKE-1", "target_identifier": "KEY-1",
        "primary_metric": 10.0, "secondary_metric": 5.0,
        "status_descriptor": "NOMINAL", "is_critical_flag": False,
    }
    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200
    assert response.json()["overall_urgency"] == "ROUTINE"
    payload["attributes"] = {"notes": "Patient MRN-994827"}
    assert client.post("/api/audit", json=payload).status_code == 422
    response = client.get("/metrics/prometheus")
    assert response.status_code == 200
    assert "system_tasks_total" in response.text


def test_mock_does_not_pretend_to_use_remote_llms():
    from agents.llm_factory import LLMFactory
    assert "No language-model inference" in LLMFactory.create().invoke("test")
    with pytest.raises(ValueError, match="not implemented"):
        LLMFactory.create("openai")


def test_browser_script_syntax():
    content = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    match = re.search(r"<script>(.*?)</script>", content, re.S)
    assert match, "Standalone console must include a script"
    assert "not</strong> ESM-2 inference" in content
    assert "model_inference: false" in content
    if shutil.which("node") is None:
        pytest.skip("Node.js not installed; static script syntax not checked")
    result = subprocess.run(
        ["node", "--check", "-"],
        input=match.group(1), text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr
