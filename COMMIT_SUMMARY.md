# Commit Message Summary & Suggested Commands

Use these concise commit messages to form a clear history for reviewers. Apply them in sequence during your final push.

1) "chore: scaffold project structure and sample docs"
   - initial layout: `src/`, `data/docs/`, `tests/`, `eval/`, `assets/`

2) "feat: add TF-IDF retriever and pipeline"
   - implemented retrieval logic and pipeline orchestration

3) "test: add unit tests for retriever and pipeline"
   - basic tests for retrieval and pipeline confidence

4) "feat: add mock generator and CLI"
   - deterministic generator for reproducible outputs; CLI entrypoint

5) "feat: add openai generator stub and mocked test"
   - safe LLM integration with environment checks; added mocked test

6) "feat: add evaluation harness and ground-truth"
   - evaluate accuracy and mean confidence across sample queries

7) "chore: add CI workflow and project docs"
   - GitHub Actions to run tests; README and model_card updates

Suggested git commands (run from repo root):

```bash
git init
git add .
git commit -m "chore: scaffold project structure and sample docs"
git add src/retriever.py src/system.py src/generator.py
git commit -m "feat: add TF-IDF retriever and pipeline"
git add tests/
git commit -m "test: add unit tests for retriever and pipeline"
git add src/cli.py
git commit -m "feat: add mock generator and CLI"
git add src/generator.py tests/test_generator_openai.py requirements.txt
git commit -m "feat: add openai generator stub and mocked test"
git add eval/
git commit -m "feat: add evaluation harness and ground-truth"
git add .github README.md model_card.md PORTFOLIO.md
git commit -m "chore: add CI workflow and project docs"
git remote add origin <YOUR_REPO_URL>
git branch -M main
git push -u origin main
```

Replace `<YOUR_REPO_URL>` with your GitHub repo URL. These messages keep changes small and review-friendly.
