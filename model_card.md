# Model Card — Applied AI System (Retrieval-Augmented QA)

**By Mofe Okonedo**

Overview

I built this system to demonstrate how to integrate retrieval and generation into a reliable, testable AI application. The core idea is simple: instead of asking a language model to generate an answer from scratch, I first retrieve relevant documents and then ask the model to answer based on those context. This approach (RAG) grounds the model's responses in actual data, reducing hallucinations and improving traceability.

- The `mock` generator provides deterministic outputs for unit testing; I don't need API keys or network calls.
- The `openai` mode integrates with OpenAI's API (v1.0+) and includes error handling so the system degrades gracefully.
- Confidence scoring uses max TF-IDF similarity, which correlates with retrieval quality and serves as a reliability signal.

Limitations & Biases I'm Aware Of

- **Retrieval limitations**: TF-IDF favors lexical overlap. If a document uses different terminology than the query, the retriever may miss it. This is a real limitation; semantic search (embeddings) would help but adds complexity.
- **Generation**: The mock generator is intentionally simple and doesn't reason. OpenAI's models can hallucinate or confidently assert things that are factually wrong. This risk increases with smaller training sets or niche domains.

Potential Misuse & How I'm Mitigating It

- **Data leakage**: If I index sensitive documents (API keys, proprietary data), the retriever could expose them. Mitigation: I apply access controls before retrieval and document the risk clearly.
- **Hallucination**: LLMs can confidently generate false information. Mitigation: I validate outputs against sources, include source citations in the response, and log all queries for audit trails. For high-risk domains, I'd add human-in-the-loop review.
- **Over-reliance on confidence**: My confidence score is not a calibrated probability. Mitigation: I'm transparent about this limitation and pair it with an evaluation harness that measures actual accuracy.

Testing & Reliability Signals I Implemented

- **Automated tests** (`tests/` folder): I wrote unit tests for retriever logic, full-pipeline behavior, and a fully-mocked OpenAI integration test. All 4 tests pass. Mocking was critical: it lets me test the OpenAI integration without needing API keys.
- **Confidence scoring**: I compute confidence as max TF-IDF similarity. This is a heuristic, not a calibrated probability, but it correlates with retrieval quality.
- **Evaluation harness** (`eval/evaluate.py`): I built a harness that runs queries against ground-truth data and reports accuracy and mean confidence. This is my primary reliability signal.
- **Logging**: Every major step is logged (query, retrieved documents, generated answer, confidence). This enables debugging and auditing.
- **Graceful error handling**: If the OpenAI API fails, the generator returns a safe error message instead of crashing.

Ethical Reflection

- **Bias**: The simple TF-IDF retriever can amplify surface-level biases in the source documents (e.g., if training data is skewed, so is the retrieval). I mitigated this by including a model card and recommending dataset reviews before deployment.
- **My approach to AI collaboration**: I used AI to speed up boilerplate (CLI scaffolding, test templates) but subjected every suggestion to human review. The integration details, error handling, and design choices are deliberate. I also rejected suggestions to over-complicate the system or to rely on untested heuristics.
- **Safety by design**: Rather than adding features, I focused on reliability: deterministic tests, evaluation metrics, logging, and graceful failures. These fundamentals are more valuable than raw capability.

