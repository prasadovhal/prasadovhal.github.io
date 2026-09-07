"""
Run from the repo root:
    pip install wordcloud matplotlib
    python generate_wordcloud.py
Overwrites images/wordcloud/wc6.png in place.
"""

import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ---------------------------------------------------------------------------
# Term weights — hand-curated, not scraped from bio prose.
# Higher number = larger in the cloud.
# ---------------------------------------------------------------------------
frequencies = {
    # ── Current core expertise ──────────────────────────────────────────────
    "Large Language Models":          100,
    "Retrieval-Augmented Generation":  95,
    "Agentic AI":                       90,
    "Generative AI":                    85,
    "LLM Evaluation":                   78,
    "Model Context Protocol":           75,
    "Hybrid Retrieval":                 70,
    "Vector Search":                    68,
    "Hallucination Detection":          65,
    "Prompt Engineering":               62,
    "RAG":                              60,

    # ── ML / Data Science foundations ───────────────────────────────────────
    "Machine Learning":                 82,
    "Data Science":                     78,
    "Deep Learning":                    62,
    "Natural Language Processing":      60,
    "Time Series Forecasting":          58,
    "Predictive Modeling":              52,
    "Feature Engineering":              50,
    "Bayesian Methods":                 45,
    "MLOps":                            48,

    # ── Research specialisation ──────────────────────────────────────────────
    "Feature Selection":                55,
    "Black Hole Algorithm":             52,
    "Stochastic Optimization":          48,
    "Genetic Algorithm":                42,
    "Simulated Annealing":              38,
    "Ant Colony Optimization":          35,
    "Optimization":                     40,

    # ── Tools & infrastructure ───────────────────────────────────────────────
    "Python":                           58,
    "PyTorch":                          42,
    "HuggingFace":                      44,
    "LangChain":                        42,
    "LangGraph":                        38,
    "FAISS":                            36,
    "BM25":                             33,
    "OpenShift":                        30,
    "Docker":                           28,
    "SQL":                              30,

    # ── Domain experience ────────────────────────────────────────────────────
    "Cybersecurity":                    38,
    "Credit Risk":                      34,
    "Bioinformatics":                   34,
    "Forecasting":                      40,
    "NLP":                              45,
    "Transformers":                     42,
    "AI Research":                      50,
    "Production AI":                    52,
    "Red Hat":                          50,
    "Teaching":                         38,
    "Research":                         42,
}

# ---------------------------------------------------------------------------
# Color palette — vibrant multi-colour, grouped by hue family
# ---------------------------------------------------------------------------
BLUES    = ["#0D47A1", "#1976D2", "#0288D1", "#039BE5"]
TEALS    = ["#00838F", "#0097A7", "#00ACC1", "#00BCD4"]
GREENS   = ["#2E7D32", "#388E3C", "#43A047", "#00897B"]
PURPLES  = ["#6A1B9A", "#7B1FA2", "#8E24AA", "#AB47BC"]
ORANGES  = ["#E65100", "#EF6C00", "#F57C00", "#FB8C00"]
REDS     = ["#B71C1C", "#C62828", "#D32F2F", "#E53935"]

ALL_COLOURS = BLUES + TEALS + GREENS + PURPLES + ORANGES + REDS

# Each word gets a colour drawn from one hue family, chosen by word hash
# so the same word always gets the same colour family (stable across runs)
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    families = [BLUES, TEALS, GREENS, PURPLES, ORANGES, REDS]
    family = families[hash(word) % len(families)]
    return random.choice(family)


wc = WordCloud(
    width=1400,
    height=700,
    background_color="white",
    color_func=color_func,
    max_words=60,
    prefer_horizontal=0.75,
    min_font_size=11,
    max_font_size=130,
    collocations=False,       # prevents splitting compound terms
    random_state=42,
    margin=8,
).generate_from_frequencies(frequencies)

fig, ax = plt.subplots(figsize=(14, 7), facecolor="white")
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
plt.tight_layout(pad=0)

out = "images/wordcloud/wc6.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
