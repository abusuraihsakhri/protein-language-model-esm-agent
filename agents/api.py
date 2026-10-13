"""
FastAPI REST API Server for Protein Language Model Esm Agent.
"""
import os
import secrets
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .metrics import GLOBAL_METRICS
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Protein Language Model Esm Agent API",
    description="Demonstration of deterministic threshold checks; no protein-model inference",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "protein-language-model-esm-agent", "domain": "AI Drug Discovery, Structural Biology & Wet-Lab Robotics", "standard": "Demonstration thresholds; not ESM-2 inference", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException:
        raise HTTPException(status_code=422, detail="Sensitive identifier pattern detected")
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException:
        raise HTTPException(status_code=422, detail="Sensitive identifier pattern detected")


@app.get("/metrics/prometheus", response_class=PlainTextResponse)
def prometheus_metrics():
    return GLOBAL_METRICS.export_prometheus_text()


@app.get("/api/audit/logs")
def api_audit_logs(x_audit_token: str | None = Header(default=None)):
    """Disable audit-log reads unless a dedicated access token is configured."""
    expected = os.getenv("AUDIT_LOG_TOKEN", "")
    if not expected:
        raise HTTPException(status_code=503, detail="Audit-log access is disabled")
    if not x_audit_token or not secrets.compare_digest(x_audit_token, expected):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
