"""
FastAPI REST API Server for ProteinLM-Embedding: Masked Language Model Perplexity & Mutational Fitness Agent.
"""
from typing import Dict, Any
from .models import FrontierPayload
from .agents import ProteinLMCoordinator

coordinator = ProteinLMCoordinator()


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel

        app = FastAPI(
            title="ProteinLM-Embedding: Masked Language Model Perplexity & Mutational Fitness Agent",
            description="Computes residue log-likelihood ratios (LLR) and evolutionary fitness landscapes for deep mutational scanning (DMS) variants.",
            version="2.0.0-FRONTIER",
        )

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "protein-language-model-esm-agent", "domain": "Biomedical Scientific Discovery & Multi-Omics", "version": "2.0.0-FRONTIER"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
