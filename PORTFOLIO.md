# Portfolio Blurb — Applied AI System (Retrieval‑Augmented QA)

This project demonstrates an end-to-end Retrieval‑Augmented Question Answering system built from a Module 1–3 prototype and extended for reliability. It combines a lightweight TF‑IDF retriever with a pluggable generator (deterministic `mock` and an `openai` stub), automated tests, a small evaluation harness, and CI to ensure reproducibility.

Highlights
- AI feature: Retrieval‑Augmented Generation (RAG) — the system retrieves top document contexts and conditions generation on them.
- Reliability: confidence scoring (max similarity), unit tests, an evaluation harness with ground truth, and CI testing.
- Safety: generator degrades gracefully when external LLMs fail; guidance and a `model_card.md` describe limitations and mitigations.

Try it

```bash
source ~/project/venv/bin/activate
python -m project.src.cli "What is Python used for?"
```

Why this project belongs in a portfolio
- Demonstrates system integration thinking: retriever → generator → evaluator.
- Shows testing and reliability practices: mocked external APIs, automated tests, evaluation metrics, and CI.
- Production-minded: pluggable LLM integration, logging, and clear documentation for reviewers.

Files to review
- `src/` — core implementation
- `tests/` — unit tests and mocked OpenAI test
- `eval/` — evaluation harness and ground truth
- `model_card.md` — reflections, biases, and mitigations
- `assets/diagram.mmd` — architecture diagram
