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

Routing a support ticket correctly, finding the right answer, and executing account actions safely are three problems that most systems solve in isolation. This project treats them as one pipeline. A LangGraph agent classifies intent using one of 15 trained scikit-learn models, retrieves context through a hybrid BM25 and pgvector search, applies deterministic policy rules, and routes high-risk operations to human approvers. The data foundation is 1,000 support tickets across four channels and 90 knowledge documents chunked into 185 passages. Full architecture and benchmarks in [project_overview.md](https://github.com/prasadovhal/customer-support-platform/blob/main/docs/project_overview.md).

**Architecture at a Glance**

The data layer is 1,000 support tickets (22 attributes, July 2024-December 2025, 4 channels) and 90 knowledge documents chunked into 185 retrievable passages. On top of that, TF-IDF paired with three classifiers runs across 5 tasks, producing 15 trained models covering category, priority, sentiment, escalation, and routing. Retrieval combines BM25 and pgvector HNSW dense search, merges candidates via Reciprocal Rank Fusion, reranks with a cross-encoder, and passes the top-5 passages to the LLM. The agent is a LangGraph 4-node state graph (classify, retrieve, handle_action, generate) with conditional branching and a keyword-heuristic fallback. The policy engine applies stateless deterministic rules for refunds, cancellations, and account changes, with high-risk actions routed to a human approval queue via Celery Beat. Observability covers Prometheus, LangFuse, and OpenTelemetry to Jaeger; the CI regression gate blocks on more than 5% degradation in Recall@5, nDCG@5, or MRR.

**Machine Learning Pipelines (15 trained models across 5 classification tasks)**

The feature pipeline is TF-IDF (10k features, unigram+bigram, sublinear TF) paired with three classifiers (Logistic Regression, Random Forest, Gradient Boosting) across five tasks: category, priority, sentiment, escalation, and routing. Split is stratified 60/20/20 on 1,000 tickets.

Routing reached 97.0% test accuracy, macro-F1 0.845 across 7 support teams. Escalation (binary, 85/15 split) reached 54.5-80% with class-balanced weighting, P0 recall up to 33%. Priority (4-class) sits at 30-43.5%, with P0 at only 2.9% of the dataset.

`class_weight='balanced'` was applied for priority, sentiment, and escalation. Sentiment (23.5-40% accuracy, macro-F1 0.236-0.248) and priority are near-random; the root cause is that synthetic ticket bodies carry no label signal, only subject lines do.

**Hybrid Retrieval-Augmented Generation (RAG) Architecture**

The retrieval pipeline combines BM25 (rank-bm25, in-memory, 185 chunks) with dense vector search (BAAI/bge-base-en-v1.5, 768-dim, L2-normalized, HNSW index on pgvector). Candidates from both systems are merged using Reciprocal Rank Fusion (K=60), then reranked with a cross-encoder (ms-marco-MiniLM-L-6-v2) before the top-5 passages go to the LLM.

Evaluated on 62 queries: Recall@5 = 0.503, Recall@10 = 0.653, MRR = 0.388, nDCG@5 = 0.389, Precision@5 = 0.123. Chunk size is 1,500 chars (~400 tokens) with 200-char overlap; context budget per response is 6,000 chars.

Retrieval by difficulty: Easy (n=16) Recall@5 = 0.604, MRR = 0.375; Medium (n=28) 0.500, 0.400; Hard (n=14) 0.536, 0.492; Adversarial (n=4) 0.000, 0.000.

**Generation Quality and LLM-as-a-Judge Evaluation**

Groundedness was evaluated on 70 golden QA pairs using BM25 context. Mean context coverage was 0.594. Only 30% of responses (21/70) met the grounded threshold (coverage >= 0.70), and 5.7% (4/70) were flagged as hallucination risk (coverage < 0.30).

LLM-as-a-Judge scoring (Mistral judge, 15 QA pairs): Faithfulness 4.2/5.0 (84%), Answer Relevance 4.3/5.0 (87%), Correctness 4.1/5.0 (81%). Heuristic proxies (token-F1 = 0.074, Jaccard = 0.110) scored far lower because they measure lexical overlap, not paraphrase quality. For paraphrase-heavy outputs, judge-based scoring is the more reliable signal.

**Agentic LangGraph Workflow and Intent Classification**

The agent runs as a 4-node LangGraph state graph (classify, retrieve, handle_action, generate) with conditional branching at each step. The ML intent classifier reached 60.0% accuracy (24/40 free-text messages). A keyword-heuristic fallback scored 78.0% (39/50 scenarios), so both are wired in, with the heuristic taking priority for most intents.

On a 50-scenario eval set: retrieval routing 100% (50/50), greeting skip rate 100% (4/4), approval routing 62.0% (31/50), policy compliance 100%. End-to-end workflow passes 21/21 with mocked intent across all 12 use cases.

**Policy Engine and Human-in-the-Loop Approvals**

The policy engine is stateless and deterministic. Refunds auto-approve up to $50/$100/$200 depending on customer segment, and are denied if the order is older than 30 days. Cancellations auto-approve for pending or processing orders, are denied for delivered or already-cancelled orders, and require approval if shipped. Account and email changes always require approval.

Pending approvals expire via Celery Beat. Every decision is logged to a PostgreSQL `audit_log` table with UUID, timestamp, actor, action, and reason. The Ollama LLM client uses a circuit breaker with 3-attempt exponential backoff.

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
5. **Start the API** (interactive docs at `http://localhost:8000/docs`)
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

**Observability and MLOps**

Observability runs across three tools. Prometheus handles HTTP latency histograms and call counts for agent, LLM, and RAG operations. LangFuse traces each request with child spans across classify, retrieve, handle, and generate steps, including groundedness correlation. OpenTelemetry feeds Jaeger for infra-level spans across FastAPI, SQLAlchemy, Redis, Celery, and httpx.

The GitHub Actions pipeline runs ruff lint, mypy type checking, 158 unit tests, and 43 integration tests. A retrieval regression gate blocks the build if Recall@5, nDCG@5, or MRR degrades more than 5% from baseline. The final step builds Docker images for all services.

**What This Demonstrates**

**Evaluation framework design:** Different system layers need different metrics. Retrieval uses Recall@K, MRR, and nDCG. Generation uses context coverage and LLM-as-a-Judge scoring. Classifiers are evaluated per class. Heuristic proxies (token-F1 = 0.074, Jaccard = 0.110) were measured, found unreliable for paraphrase-heavy outputs, and replaced with judge-based assessment.

**Honest benchmarking:** Priority (30-43%) and sentiment (23-40%) classifiers perform near-random on this dataset. The root cause is documented: synthetic ticket bodies carry no label signal, only subject lines do. These results are presented as evidence for real data collection, not discarded.

**Full-stack system design:** The project covers every layer: raw data (1,000 tickets, 22 attributes), feature engineering, 15 classification models, hybrid retrieval with pgvector and BM25, a LangGraph agent, a deterministic policy engine, and a three-tool observability stack. Each layer is evaluated against defined targets.

**Production MLOps:** The CI pipeline blocks on retrieval metric regression. The LLM client has a circuit breaker. Approval expiry is managed by Celery Beat. Every policy decision is audit-logged. These are not afterthoughts; they were scoped as first-class requirements.

**Architecture decisions:** RRF was chosen over learned fusion to avoid a dependency on labeled retrieval data. The keyword heuristic was chosen over the ML classifier after measuring 60% vs. 78% accuracy on the eval set. Policy rules were implemented as stateless logic rather than LLM prompts to guarantee deterministic compliance. All 13 key decisions are documented in Architecture Decision Records.
