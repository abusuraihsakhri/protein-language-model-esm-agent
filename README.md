# Protein Language Model Esm Agent

> **Domain:** Computational Biology & AI Drug Discovery
> **Reference Guidelines & Standards:** `wwPDB, IUPAC & CLSI Computational Guidelines`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Protein Language Model Esm Agent** is an analytical platform implementing ESM-2 masked language model residue log-likelihood ratio and DMS (Deep Mutational Scanning) fitness prediction. It provides a multi-agent architecture with specialized workers for quality control, safety escalation, and protocol conformance evaluation.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Computes residue log-likelihood ratios and mutational fitness scores with configurable thresholds.
- **Multi-Agent Worker Architecture**: Specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) evaluate payloads independently.
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED_RISK, CRITICAL_STAT_PANIC) with automated action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking, anomaly detection, and PHI outbound protection.
- **Enrichment Suite**: Domain-specific engines for Variant, Protein, Enzyme, Antibody, Ancestral sequence reconstruction, and Drug target analysis.

---

## 🚀 Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/protein-language-model-esm-agent.git
cd protein-language-model-esm-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# (Optional) Configure environment variables
cp .env.example .env
# Edit .env to set AUDIT_SECRET_KEY for production
```

### Environment Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `AUDIT_SECRET_KEY` | HMAC-SHA256 key for audit trail signing | Randomly generated (warns if unset) |
| `MODEL_PROVIDER` | LLM backend: `mock`, `ollama`, `claude`, `openai` | `mock` |

---

## 💻 CLI Quickstart & Usage

### 1. Run a Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What standard is applied?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Input Data Schema

| Field | Type | Description | Requirement |
|:------|:-----|:------------|:------------|
| `task_id` | str | Unique task / case identifier | Required |
| `target_identifier` | str | Entity, specimen, or target key | Required |
| `primary_metric` | float | Primary domain measurement or score | Required |
| `secondary_metric` | float | Secondary kinetic or confidence score | Optional (default: 0.0) |
| `status_descriptor` | str | Status code or phenotype descriptor | Optional (default: "NOMINAL") |
| `is_critical_flag` | bool | Emergency escalation trigger | Optional (default: false) |

---

## 🛡️ Security & Architecture

- **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOB, and patient identifiers from outbound data.
- **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. Each entry links to the previous hash.
- **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances, Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
- **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
- **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:
```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:
```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

### Docker
```bash
docker build -t protein-language-model-esm-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key protein-language-model-esm-agent
```

### Docker Compose
```bash
# Set your audit secret key
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

docker compose up --build
```

---

## 📁 Project Structure

```
├── agents/                  # Multi-agent orchestration core
│   ├── __init__.py          # Package metadata
│   ├── api.py               # FastAPI REST endpoints
│   ├── base.py              # Security, PHI guard, HMAC audit
│   ├── learning.py          # Bayesian calibration engine
│   ├── llm_factory.py       # LLM provider abstraction
│   ├── metrics.py           # Prometheus metrics collector
│   ├── models.py            # Pydantic data models
│   ├── streamer.py          # WebSocket telemetry broadcaster
│   ├── supervisor.py        # Master coordinator
│   └── workers.py           # Specialized evaluation workers
├── protein_lm_agent/        # Frontier ESM-2 agent package
│   ├── agents.py            # Sub-agents (MaskedResidue, LogLikelihoodRatio, EvolutionaryFitness)
│   ├── cli.py               # Frontier CLI
│   ├── engine.py            # Core algorithmic engine
│   ├── models.py            # Frontier data models
│   └── server.py            # Frontier FastAPI server
├── tests/                   # Pytest test suite
│   ├── test_enrichment.py
│   ├── test_protein_language_model_esm_agent.py
│   └── test_protein_lm_agent.py
├── web/index.html           # Operations console UI
├── cli.py                   # Main CLI entry point
├── enrichment.py            # Domain enrichment engines
├── simulator.py             # High-throughput stress tester
├── Dockerfile               # Container definition
├── docker-compose.yml       # Compose orchestration
└── pyproject.toml           # Project metadata & dependencies
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
