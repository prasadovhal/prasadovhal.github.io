---
title: "Enterprise Customer Support AI Platform"
collection: projects
type: "Industry Project"
permalink: /projects/customer-support-platform
venue: "Personal / Open Source"
date: 2026-09-01
location: "Pune, Maharashtra, India"
link: "https://github.com/prasadovhal/customer-support-platform"
---

Customer support operations at scale face three compounding challenges: accurate intent routing, context-aware knowledge retrieval, and safe execution of account-level actions without over-automation. This platform addresses all three — classifying support tickets with 15 scikit-learn pipelines, retrieving answers through a hybrid BM25 + dense vector RAG system, and orchestrating actions through a LangGraph agent that enforces deterministic policy rules and escalates high-risk operations to human approvers. Built across 1,000 structured tickets and 90 knowledge documents, it serves as a production-grade reference system demonstrating Principal Data Scientist depth: end-to-end ML evaluation, retrieval benchmarking with Recall/MRR/nDCG, LLM-as-a-Judge quality assessment, and CI regression gates that block deployments on metric degradation. Full architecture and benchmark details in [project_overview.md](https://github.com/prasadovhal/customer-support-platform/blob/main/docs/project_overview.md).

**Architecture at a Glance**
* **Data layer:** 1,000 support tickets (22 attributes, July 2024–December 2025, 4 channels) + 90 knowledge documents chunked into 185 retrievable passages
* **ML pipelines:** TF-IDF (10k features) → {Logistic Regression, Random Forest, Gradient Boosting} × 5 classification tasks = 15 trained models (category, priority, sentiment, escalation, routing)
* **Hybrid RAG:** BM25 (in-memory) + pgvector HNSW dense search → Reciprocal Rank Fusion → cross-encoder reranking → top-5 context passages passed to LLM
* **Agent orchestration:** LangGraph 4-node state graph (classify → retrieve → handle_action → generate) with conditional branching and keyword-heuristic fallback
* **Policy engine:** Stateless deterministic rules for refunds, order cancellations, and account changes; high-risk actions routed to human approval queue via Celery Beat with audit trail
* **Observability:** Prometheus metrics + LangFuse LLM tracing + OpenTelemetry → Jaeger; GitHub Actions CI regression gate blocks on >5% degradation in Recall@5, nDCG@5, or MRR

**Machine Learning Pipelines (15 trained models across 5 classification tasks)**
* Built TF-IDF (10k features, unigram+bigram, sublinear TF) → {Logistic Regression, Random Forest, Gradient Boosting} pipelines for intent category, priority, sentiment, escalation, and routing classification; stratified 60/20/20 train-val-test split on 1,000 support tickets with 22 attributes.
* Routing classifier: 97.0% test accuracy, macro-F1 0.845 across 7 support teams; escalation binary classifier: 54.5–80% accuracy with class-balanced weighting on 85/15 split; priority 4-class: 30–43.5% accuracy with P0 recall up to 33% on severely imbalanced data (P0 = 2.9%).
* Applied `class_weight='balanced'` strategy for priority, sentiment, and escalation tasks; documented signal-weakness root cause for synthetic-data near-random performance on sentiment (23.5–40% accuracy, macro-F1 0.236–0.248).

**Hybrid Retrieval-Augmented Generation (RAG) Architecture**
* Designed BM25 (rank-bm25, in-memory, 185 chunks) + dense vector search (BAAI/bge-base-en-v1.5, 768-dim, L2-normalized, HNSW index on pgvector) → Reciprocal Rank Fusion (K=60) → cross-encoder reranking (ms-marco-MiniLM-L-6-v2) pipeline over 90 knowledge documents.
* Evaluated over 62 queries: Recall@5 = 0.503, Recall@10 = 0.653, MRR = 0.388, nDCG@5 = 0.389; Precision@5 = 0.123; chunk size 1,500 chars (~400 tokens) with 200-char overlap; context budget 6,000 chars per response.
* Retrieval difficulty breakdown: Easy (n=16) Recall@5 = 0.604 / MRR = 0.375; Medium (n=28) 0.500 / 0.400; Hard (n=14) 0.536 / 0.492; Adversarial (n=4) 0.000 / 0.000.

**Generation Quality & LLM-as-a-Judge Evaluation**
* Conducted groundedness evaluation over 70 golden QA pairs (BM25 context): mean context coverage 0.594, grounded rate (coverage ≥ 0.70) = 30% (21/70), hallucination-risk rate (coverage < 0.30) = 5.7% (4/70).
* LLM-as-a-Judge (Mistral judge, 15 QA pairs): Faithfulness 4.2/5.0 (84%), Answer Relevance 4.3/5.0 (87%), Correctness 4.1/5.0 (81%); identified systematic underestimation by heuristic token-F1 (0.074) and Jaccard (0.110) proxies vs. LLM-judge paraphrase recognition.

**Agentic LangGraph Workflow & Intent Classification**
* Orchestrated a 4-node LangGraph state graph (classify → retrieve → handle_action → generate) with conditional branching; intent ML classifier: 60.0% accuracy (24/40 free-text messages); keyword-heuristic fallback: 78.0% accuracy (39/50 scenarios).
* Routing performance (50-scenario eval set): retrieval routing 100% (50/50), greeting skip rate 100% (4/4), approval routing 62.0% (31/50), policy compliance 100%; end-to-end workflow: 21/21 (100%) pass rate with mocked intent across all 12 use cases.

**Policy Engine & Human-in-the-Loop Approvals**
* Implemented deterministic stateless policy engine for refund (auto-approve ≤$50/$100/$200 by customer segment; deny if order age > 30 days), order cancellation (auto-approve if status ∈ {pending, processing}; deny if delivered/cancelled/refunded), and account/email changes (always require approval).
* Built Celery Beat approval expiration workflow; full audit trail to PostgreSQL `audit_log` table with UUID, timestamp, actor, action, and reason; circuit breaker + 3-attempt exponential-backoff on Ollama LLM client.

**Run It Yourself — Step-by-Step Setup**

Full guide: [docs/deployment/local_setup.md](https://github.com/prasadovhal/customer-support-platform/blob/main/docs/deployment/local_setup.md)

1. **Clone & install dependencies**
   ```bash
   git clone https://github.com/prasadovhal/customer-support-platform.git
   cd customer-support-platform
   poetry install --with dev
   ```
2. **Start infrastructure** (PostgreSQL 15 + pgvector, Redis)
   ```bash
   docker compose up db redis -d
   # Confirm health: docker compose ps
   ```
3. **Configure environment**
   ```bash
   cp .env.example .env
   # Set DATABASE_URL, REDIS_URL, and JWT_SECRET_KEY=$(openssl rand -hex 32)
   ```
4. **Run database migrations**
   ```bash
   poetry run alembic upgrade head
   ```
5. **Start the API** — interactive docs at `http://localhost:8000/docs`
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```
6. **Optional: add local LLM (Ollama / llama3.2)**
   ```bash
   docker compose --profile llm up ollama -d
   ollama pull llama3.2
   ```
7. **Verify with tests** (158 unit + 43 integration)
   ```bash
   poetry run pytest tests/unit/ -q
   TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/customer_support_test \
     poetry run pytest tests/integration/ -q
   ```

**Observability & MLOps**
* Three-layer observability: Prometheus metrics (HTTP latency histograms, agent/LLM/RAG call counts, approval outcomes), LangFuse LLM tracing (per-request traces with classify/retrieve/handle/generate spans and groundedness correlation), OpenTelemetry → Jaeger infra spans (FastAPI, SQLAlchemy, Redis, Celery, httpx, 16-char trace IDs).
* CI/CD regression gate in GitHub Actions: Recall@5, nDCG@5, MRR with ≤5% degradation tolerance; 158 unit tests + 43 integration tests (179 total); ruff lint + mypy type checking; Docker multi-service build (FastAPI, PostgreSQL 15 + pgvector, Redis, Celery).

**What This Demonstrates**
* **Evaluation framework design:** Defined the right metrics at each layer — Recall@K/MRR/nDCG for retrieval, coverage + LLM-as-a-Judge for generation, accuracy/F1 per class for classifiers — rather than relying on a single aggregate score; identified where heuristic proxies (token-F1 = 0.074, Jaccard = 0.110) systematically mislead and replaced them with judge-based assessment.
* **Intellectual honesty in benchmarking:** Priority (30–43%) and sentiment (23–40%) classifiers perform near-random; rather than discarding these results, the project diagnoses the root cause (synthetic data encodes label only in subject line, not body), documents it, and uses it to argue for real data collection — the kind of honest trade-off reasoning expected at principal level.
* **Full-stack ML system design:** Owns every layer from raw data (1,000 tickets, 22 attributes) through feature engineering, model training, hybrid retrieval, agent orchestration, policy enforcement, and production observability — demonstrating breadth without losing depth at any layer.
* **Production MLOps thinking:** Regression gates that block CI on metric degradation, circuit breakers on LLM calls, Celery-managed approval expiry, structured audit logging, and a three-signal observability stack reflect operational maturity beyond model accuracy.
* **Principled architecture trade-offs:** Chose RRF over learned fusion to avoid training data dependency on retrieval; chose keyword-heuristic fallback over a pure ML classifier after measuring 60% vs. 78% accuracy; chose stateless policy rules over an LLM for deterministic compliance — each decision documented in 13 Architecture Decision Records.
