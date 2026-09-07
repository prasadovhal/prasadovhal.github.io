---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
---

Education
======
* M.Tech in Mathematical Modelling & Simulation (Data Science), Centre for Modeling & Simulation, Savitribai Phule Pune University — 2019
* B.E. in Mechanical Engineering, Pimpri Chinchwad College of Engineering, Savitribai Phule Pune University — 2015

Work Experience
======
* **Oct 2024 – Present · Senior Data Scientist** — Red Hat India
  * Building an AI-powered intelligence engine providing support engineers with relevant customer issue context; owning the data pipeline, subgraph, and vector database services while supporting LLM integration and evaluation.
  * Conducting retrieval and LLM evaluations using LLM-as-a-Judge to measure search quality and answer accuracy; building automated golden datasets via similarity matching and LLM-based relevance evaluation (LLM Avg Precision@2: 82–86%).
  * Evaluating document chunking strategies to improve retrieval performance (Avg Precision@2: 50% → 65%, Avg Recall@2: 60% → 72%).
  * Technical Lead for SBR Routing and Tagging systems — driving architecture, rule-engine design, and ML model enhancements to increase coverage (SBR: 88% → 92%, Tagging: 70% → 72%) and reduce error rates across support case workflows.
  * Managing machine translation project using transformer-based models and LLMs for multilingual document translation; optimised prompts and evaluated with BLEU-L (38%) and ROUGE-L (Precision 60%, Recall 52%).
  * Core member of the Pune AI Tiger Team, driving AI enablement across the organisation and partnering with cross-functional teams on site-level operational challenges.

* **Nov 2023 – Oct 2024 · Senior Data Scientist** — Fractal Analytics
  * Led advanced analytics for global CPG clients covering pricing, demand forecasting, and consumer insights.
  * Built Price & Weight Elasticity, Demand Transference, and Price Pack Architecture (PPA) optimization models scaled across international markets.
  * Implemented MLOps pipelines and parallel processing frameworks to improve runtime efficiency.
  * Built NLP pipelines for social media analytics — sentiment analysis, topic modelling, and Generative AI-based consumer insight extraction.

* **Aug 2019 – Nov 2023 · Data Scientist** — Red Hat India
  * Built time series forecasting systems for global financial metrics: Sales (MAPE 3%), Commissions (7%), Expenses (6%), Billings (4%), Par-rate (1.15%).
  * Developed Bayesian models for services consumption probability to support sales portfolio optimization.
  * Designed Champion–Challenger evaluation frameworks; applied hierarchical and grouped forecasting with reconciliation.
  * Developed an internal Python library for time series forecasting; implemented CI/CD pipelines via GitLab and OpenShift.
  * Worked on highly imbalanced datasets (97:3) using feature engineering, model validation, and backtesting.

* **Dec 2018 – Aug 2019 · Data Science Intern** — CRISIL India
  * Built a Credit Risk Modeling Tool in Python Dash for automated scorecard generation.
  * Applied ML and statistical techniques for credit risk assessment; integrated model interpretability for black-box models as part of M.Tech thesis.

* **Jul 2015 – Jul 2016 · Graduate Apprentice Trainee** — SKF Bearings India
  * Led shop-floor operations as Channel Team Engineer; implemented SMED, Kaizen, and 5S manufacturing practices.

Skills
======
**Generative AI & LLMs** — Agentic AI, Large Language Models, RAG, Hybrid Retrieval (BM25 + Dense), Vector Search, Re-ranking, LLM Evaluation, Hallucination Detection, Prompt Engineering, Fine-Tuning, Model Context Protocol (MCP)

**Machine Learning** — Machine Learning, Deep Learning, NLP, Time Series Forecasting, Feature Engineering, Feature Selection, Bayesian Methods, Stochastic Optimization, Model Evaluation & Validation

**Languages** — Python, R, SQL

**Libraries & Frameworks** — PyTorch, TensorFlow, Keras, HuggingFace Transformers, LangChain, LangGraph, Scikit-learn, Sktime, NLTK, Matplotlib, Seaborn, Plotly

**Infrastructure** — FAISS, Vector Databases, Docker, OpenShift, GitLab CI/CD, Tableau, Linux

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

Teaching
======
<ul>
{% for post in site.teaching reversed %}
  {% include archive-single-talk-cv.html %}
{% endfor %}
</ul>
