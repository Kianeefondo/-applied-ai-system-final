# Applied AI System — Retrieval‑Augmented QA (Final)

**By Mofe Okonedo**

Original project: Mini QA retriever (Modules 1-3) — a small retrieval + generation prototype that returned context excerpts for user queries.

For this final project, I extended that prototype into an end-to-end applied AI system with reliability checks and an optional LLM integration. This work demonstrates system integration thinking: connecting a retriever, generator, and evaluator into a cohesive pipeline that can reliably answer questions by retrieving relevant documents and conditioning generation on them.

Architecture Overview

I built a complete RAG system with three core components:

- **Retriever** (`src/retriever.py`): TF-IDF-based document search that finds the most relevant contexts for a query. This avoids heavy dependencies while remaining testable and interpretable.
- **Generator** (`src/generator.py`): Pluggable LLM wrapper with two modes. `mock` mode returns deterministic answers for testing; `openai` mode integrates with OpenAI's API and degrades gracefully on failures.
- **Pipeline** (`src/system.py`): Orchestrates retriever → generator flow and computes a confidence score (max TF-IDF similarity) as a reliability signal.
- **System diagram** (`assets/diagram.mmd`): Visual representation of the full data flow including error handling and evaluation loops.

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

Design Decisions

I made intentional choices to balance simplicity with functionality:

- **Simplicity**: I chose TF-IDF-like retrieval over embedding models to avoid heavy dependencies. This keeps the system lightweight and easy to test, which is critical for reliability.
- **Pluggable generator**: I designed the generator to support both `mock` (deterministic, for testing) and `openai` (real LLM) modes. This separation allowed me to write tests that run without API calls while still demonstrating how to integrate external services.
- **Confidence scoring**: I compute confidence as the max similarity score returned by the retriever. It's not a calibrated probability, but it's a useful reliability signal that correlates with retrieval quality.
- **Error handling**: I wrapped OpenAI API calls with try-except blocks so the system returns a safe message on failure rather than crashing.

Testing & Reliability

I implemented multiple reliability signals to ensure the system is trustworthy:

- **Unit tests** (`tests/`): I wrote tests for retriever logic, pipeline flow, and a mocked OpenAI generator test. All tests pass and use mocking to avoid external dependencies.
- **Evaluation harness** (`eval/evaluate.py`): I built a harness that runs queries against ground-truth data and reports accuracy and mean confidence across the test set.
- **Logging**: I integrated Python logging throughout the CLI and pipeline so that every major step is traced for debugging and auditing.
- **Graceful degradation**: When the external LLM is unavailable, the system returns a safe error message instead of crashing.

Reflection & Lessons Learned

- **Limitations I'm aware of**: TF-IDF favors lexical overlap and can miss semantically similar documents. The mock generator is intentionally simple and doesn't reason. Confidence is uncalibrated and shouldn't be used as a probability without further work.
- **Production risks**: When deploying an LLM, hallucinations and data leakage are real risks. I mitigated these by including error handling, logging, and documenting safe defaults in `model_card.md`.
- **What I learned**: This project taught me that reliability in AI systems comes from end-to-end thinking. Mocking external services, automated testing, and an evaluation harness were far more valuable than adding complexity. I also learned how important it is to design systems that degrade gracefully when things go wrong.

Files
- `src/` — core modules (`retriever.py`, `generator.py`, `system.py`, `cli.py`)
- `data/docs/` — sample documents
- `tests/` — pytest unit tests
- `eval/` — evaluation harness and ground-truth data
- `assets/diagram.mmd` — system diagram

