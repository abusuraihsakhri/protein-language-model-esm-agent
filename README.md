# Protein Language Model ESM Agent

Deterministic three-worker threshold auditing for research workflow demonstrations. Includes Python command-line interfaces, FastAPI, CSV batch processing, and a standalone browser application.

**Scientific scope:** Despite its historical name, this project **does not run ESM-2 inference**. It does not load protein language models or calculate embeddings, masked-residue probabilities, perplexity, mutational log-likelihood ratios, or predicted fitness. The thresholds are application-defined examples, not validated biological thresholds.

## Main features

- Three-worker evaluation: primary metric >25 (elevated), secondary metric >12 (elevated), explicit critical flag (critical), and anomaly-keyword descriptors (elevated).
- Consensus classification, in-memory task results, and HMAC-SHA256-signed audit metadata.
- Command-line single-task and CSV batch evaluation; two existing Python interfaces remain supported.
- FastAPI health, audit, chat mock, metrics, and restricted audit-log endpoints.
- Static browser evaluation with JSON export, running entirely locally.

The enrichment module provides generic threshold demonstrations, **not** protein-specific predictive models.

## Browser application

Open [web/index.html](web/index.html) directly in a modern browser. A matching root [index.html](index.html) is also included. The GitHub Pages workflow deploys the web directory from the production branch if Pages is configured to use GitHub Actions.

The browser executes the threshold logic in JavaScript, not Python, Pyodide, or PyScript. It requires no server or model downloads. Inputs and outputs remain in the page's memory; data is not sent to the Python API or another remote endpoint. Avoid entering identifiable patient data.

## Installation and CLI

Python 3.10 or later:

    python -m pip install -e .
    protein-language-model-esm-agent audit --task-id TASK-001 --target PROTEIN-A --primary 29.4 --secondary 14.8 --status DISCORDANT
    protein-language-model-esm-agent batch -i sample.csv -o results.csv
    protein-language-model-esm-agent chat "What are the specifications?"
    protein-language-model-esm-agent verify-audit
    protein-lm-frontier audit --primary 12 --secondary 4 --status NOMINAL

CSV columns: task_id, target_identifier, primary_metric, secondary_metric, is_critical_flag, status_descriptor. Boolean values accept true/false, yes/no, or 1/0, case-insensitively. Unrecognized values are rejected.

## FastAPI service

Start the local server:

    protein-language-model-esm-agent serve --host 127.0.0.1 --port 8000

Endpoints:

| Endpoint | Response |
| --- | --- |
| GET /health | Health and version metadata |
| POST /api/audit | Worker consensus dossier |
| POST /api/chat | Deterministic mock response, not an LLM inference |
| GET /metrics | JSON counters |
| GET /metrics/prometheus | Prometheus text metrics |
| GET /api/audit/logs | Signed audit entries; requires X-Audit-Token header and configured AUDIT_LOG_TOKEN |
| GET /openapi.json | Runtime-generated OpenAPI specification |

Example audit request:

    curl -s http://127.0.0.1:8000/api/audit \
      -H 'Content-Type: application/json' \
      -d '{"task_id":"TASK-001","target_identifier":"PROTEIN-A","primary_metric":14,"secondary_metric":3,"status_descriptor":"NOMINAL","is_critical_flag":false}'

Only mock/deterministic/test are implemented as provider adapters. Ollama, Claude and OpenAI calls are not implemented; unsupported choices raise an error instead of pretending to invoke those services.

## Security and privacy

Set a strong, stable AUDIT_SECRET_KEY for HMAC signing and a separate AUDIT_LOG_TOKEN to enable log reads; see [.env.example](.env.example). When unset, the HMAC signing key is generated anew on each startup. Audit logs and task registries are **in-memory only**; they are not retained across restarts. The verifier recomputes signatures for existing audit entries, but does not authenticate source payloads that are not stored.

The pattern-based identifier filter is **not** a validated de-identification method or a HIPAA compliance guarantee. Do not send identifiable patient data to the demo. An externally accessible API requires production authentication, rate limits, TLS, and data governance. The main audit endpoint has no application-level authentication; use localhost or a properly secured proxy.

## Tests and deployment

Install test dependencies and run the suite:

    python -m pip install -e ".[test]"
    python -m pytest -q

GitHub Actions executes Python compilation, tests, and CLI smoke checks on Python 3.10, 3.11, and 3.12. The browser JavaScript syntax is checked with Node.js when present. Docker usage:

    docker build -t protein-language-model-esm-agent .
    docker run --rm -p 127.0.0.1:8000:8000 -e AUDIT_SECRET_KEY=replace-with-a-strong-secret protein-language-model-esm-agent

Alternatively, configure AUDIT_SECRET_KEY and use docker compose up --build. The Compose example binds to localhost.

## License

[MIT](LICENSE).
