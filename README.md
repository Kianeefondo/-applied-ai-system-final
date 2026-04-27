# Applied AI System — Retrieval‑Augmented QA (Final)
**By Mofe Okonedo**

# Part 1: Presentation Evaluation

Mofe's final project is clearly explained where they extended the Mini QA Retriver and applied an AI system using RAG techniques. The AI is pretty important in this vase, since it will search through a set of documents and be able to efficiently answer questions through conditioning generation. The Reliability, testing and evaluation are all discussed here and it looks like all of the tests pass, and edge cases were covered through error messages rather than crashing. The design deisions are also explained to have a balance of simplicity and functionality, avoiding heavy dependncies and having safe error messages. The project is structured pretty well, such that test cases are indicated and the new added components are explained thoroughly to show their importance. One area that could be improved is also just to include a demo in the Read Me, however, everything else looks good.

# Part 2: Glow / Grow / Action Practice
**Glow**
Mofe designed the generator really well in terms of capturing for a wide array of testing, both for mock and openai testing.

**Glow**
The ReadMe is structured really well and explains the different components really well and would help people who might be interested in using this application.

**Grow**
I would like to see a distribution for the confidence scores in the Read me as well so we can better define the different logic and systems that your simulation score goes through.

**Grow**
I believe since the system does have a balanced simplified and complex logic, I would have liked for it to lean more on the complex side so explore a bit more of the options for real world usages.

**Action Steps**
I would give more examples in the Read Me just so we can have more cases of evaluations, especially one that does have a case where the application does go wrong and what would be the reason for this issue.

**Action Steps**
I would love to see a short demo walking through the system live in case someone was not able to turn through the program. 



# Part 3: AI Depth & Coaching Lens
**1. What does shallow AI integration look like in a final project?**
Shallow AI integration means limiting the LLM in this case. Some examples would be having no validation of outputs, no way to have a secondary solution when models fail, and no way for the use to actually trust the model. If this was the case, then the AI component would be able to just be replaced best with hard coded text without fundamentally changing the system's architecture or purpose.


**What signals strong, meaningful AI engineering?**
Stong and meaningful AI engineering means a system is designed around the AI's limitations. Some examples would be building confidence and reliability signals into the outpu, writing tests for AI calls, and documenting failure modes. Students would be able to articulate what decisions is the AI helping make and what would break if it were to be removed.


**Write three probing questions you would ask a student to deepen their reasoning during breakout discussions.**
1. Can you walk m through a case where the score is high but the answer is wrong? What does that tell you about the reliability signal?
2. For the mock tests, how did you create them and what did you assess in terms of each test?
3. What would this look like on an actual application for real world use? What other kinds of applications can you think of that is similar to this?

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