# Applied AI System — Retrieval‑Augmented QA (Final)

Original project: Mini QA retriever (Modules 1-3) — a small retrieval + generation prototype that returned context excerpts for user queries.

This final project extends that prototype into an end-to-end applied AI system with reliability checks and an optional LLM integration.

Architecture Overview
- The pipeline loads local documents via a TF-IDF-like retriever (`src/retriever.py`), selects top contexts, and passes them to a generator (`src/generator.py`) which can run in `mock` or `openai` mode.
- Confidence scoring: the pipeline reports a simple confidence equal to the max cosine similarity between the query and retrieved documents.
- Assets: a Mermaid diagram is available at `assets/diagram.mmd`.

Setup
1. Create and activate a venv:

```bash
python3 -m venv ~/project/venv
source ~/project/venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r ~/project/requirements.txt
```

3. Run tests:

```bash
python -m pytest -q ~/project/tests
```

Sample interactions
- Query using the mock generator (reads from `data/docs`):

```bash
python -m project.src.cli "What is Python used for?"
```

Expected (mock) output contains an `answer`, `confidence`, and `retrieved` list. Example excerpt:

```
{
	"query": "What is Python used for?",
	"answer": "Answer (mock) based on doc1_python.txt (score=0.85): Python is a high-level programming language...",
	"confidence": 0.85,
	"retrieved": [{"doc_id": "doc1_python.txt", "score": 0.85}]
}
```

- Run the evaluation harness (measures retrieval accuracy and average confidence):

```bash
python ~/project/eval/evaluate.py --docs ~/project/data/docs --out ~/project/eval/results.json
```

Design decisions
- Simplicity: a small TF-IDF-like retriever avoids heavy dependencies and is easy to test.
- Pluggable generator: `mock` mode enables deterministic tests; `openai` mode demonstrates how to integrate an external LLM with error handling.
- Confidence: derived from similarity; not a calibrated probability, but useful as a reliability signal.

Testing & Reliability
- Unit tests: `tests/` contains retriever, pipeline, and generator tests (including a mocked OpenAI test).
- Evaluation harness: `eval/evaluate.py` runs a small ground-truth set and reports accuracy and mean confidence.
- Logging: the CLI and pipeline use Python logging for traceability.

Reflection
- Limitations: TF-IDF favors lexical overlap; the mock generator is not a real LLM. Confidence is uncalibrated.
- Bias & misuse: with an external LLM, hallucinations and data leakage are risks; add filters and access controls in production.
- What I learned: adding evaluation and mocking external models greatly improves reliability and reproducibility.

Files
- `src/` — core modules (`retriever.py`, `generator.py`, `system.py`, `cli.py`)
- `data/docs/` — sample documents
- `tests/` — pytest unit tests
- `eval/` — evaluation harness and ground-truth data
- `assets/diagram.mmd` — system diagram

