# Portfolio — Applied AI System (Retrieval-Augmented QA)

**By Mofe Okonedo**

For this capstone project, I built an end-to-end Retrieval-Augmented Question Answering system that extends a Module 1–3 prototype. My implementation combines a lightweight TF-IDF retriever with a pluggable LLM generator (mock and OpenAI modes), automated unit tests, an evaluation harness, and complete documentation. I prioritized reliability, testability, and graceful error handling throughout.

Key Achievements

- **AI Integration**: I implemented true Retrieval-Augmented Generation (RAG)—the system retrieves contextual documents and conditions generation on them. This is not a surface-level integration; the data flows end-to-end and each component is testable.
- **Reliability First**: I engineered multiple reliability signals: confidence scoring (max TF-IDF similarity), automated unit tests (4/4 passing), an evaluation harness with ground-truth comparison, comprehensive logging, and graceful failure handling when the external LLM is unavailable.
- **Production-Minded Design**: I designed the generator with pluggable modes so that tests can run with deterministic mock data while production can use real OpenAI API calls. Error handling ensures the system never crashes on external failures.
- **Transparent Thinking**: I documented my design decisions, limitations, and learnings in both the README and model card so reviewers understand not just what I built, but how I thought about it.

Try It

```bash
source ~/project/venv/bin/activate
python -m src.cli "What is Python used for?"
```

Why I'm Proud of This Work

- **System Integration Thinking**: I traced the complete data flow from query → retriever → generator → confidence score → output. Each component is testable and the full pipeline is reliable.
- **Reliability & Testing Practices**: I didn't just write code; I built automated tests that mock external services, an evaluation harness with ground truth, metrics-driven development, comprehensive logging, and graceful error handling.
- **Production Mindset**: The pluggable generator design, OpenAI API v1.0+ integration, and error handling show I understand how to build systems that work in the real world.
- **Transparent Communication**: My README explains not just *what* I built but *why* I made each design choice. The model card discusses limitations, risks, and mitigations openly.

Files to Review

- `src/` — My core implementation (retriever, generator, pipeline, CLI)
- `tests/` — Automated tests including a fully-mocked OpenAI integration test
- `eval/` — Evaluation harness and ground-truth data for measuring reliability
- `model_card.md` — My detailed reflections on design choices, limitations, biases, and mitigations
- `assets/diagram.mmd` — System architecture diagram showing the complete data flow
