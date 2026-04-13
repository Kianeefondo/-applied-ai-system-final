# Model Card — Applied AI System (Demo)

Overview
This demo implements a TF-IDF-style retriever and a pluggable generator to demonstrate how retrieval-augmented QA can be integrated and tested. The `mock` generator provides deterministic outputs for unit testing; an `openai` mode shows how to plug in an external LLM with guardrails.

Limitations & Biases
- Retrieval: TF-IDF favors lexical overlap and can miss semantically relevant documents that use different vocabulary.
- Generation: the `mock` generator does not reason and only echoes context excerpts. An external LLM may hallucinate or over-confidently assert incorrect facts.

Potential Misuse & Mitigations
- Data leakage: avoid indexing sensitive documents; apply access controls and redaction before retrieval.
- Hallucination: when using an LLM, validate outputs against sources and present source citations. Include human-in-the-loop checks for high-risk outputs.

Testing & Reliability Signals
- Automated tests: unit tests cover retriever logic, pipeline flow, and an OpenAI-mocked generator test.
- Confidence scoring: uses max TF-IDF similarity as a proxy reliability signal; evaluation harness measures accuracy vs. confidence across a small ground-truth set.
- Logging and error handling: the generator returns a safe error message if the external model fails; all major steps log informational messages for debugging.

Ethical Reflection
- Limitations remain: the simple retriever can amplify surface-level biases present in source text. Any deployment must include dataset review and bias checks.
- One helpful AI suggestion during development was automated test generation; one flawed suggestion was relying solely on raw confidence as a calibrated metric.

Human-AI Collaboration Note
- This repository was scaffolded with automated assistance and then refined manually. The AI helped speed up boilerplate generation and suggested tests, but human review corrected integration details and ensured safe defaults.

