from typing import List, Tuple
import os
import logging

logger = logging.getLogger(__name__)


class Generator:
    """Pluggable generator. Supports 'mock' (deterministic) and 'openai' modes.

    For `openai` mode this class expects `OPENAI_API_KEY` to be set in the
    environment. Calls to the OpenAI API are wrapped with error handling so
    the system degrades gracefully when the API is unavailable.
    """

    def __init__(self, mode: str = 'mock'):
        self.mode = mode

    def _build_prompt(self, query: str, contexts: List[Tuple[str, str, float]]) -> str:
        prompt = """You are a concise assistant. Use the provided context excerpts to answer the query.

Context:
"""
        for doc_id, text, score in contexts:
            prompt += f"--- {doc_id} (score={score:.2f})\n{text}\n\n"
        prompt += f"Query: {query}\nAnswer succinctly and cite the most relevant doc id."""
        return prompt

    def generate(self, query: str, contexts: List[Tuple[str, str, float]]) -> str:
        if self.mode == 'mock':
            if not contexts:
                return "I don't have enough information to answer that."
            doc_id, text, score = contexts[0]
            return f"Answer (mock) based on {doc_id} (score={score:.2f}): {text[:200]}"

        if self.mode == 'openai':
            try:
                from openai import OpenAI
            except Exception as e:
                logger.error('OpenAI SDK not available: %s', e)
                raise RuntimeError('openai package required for openai mode')

            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise RuntimeError('OPENAI_API_KEY environment variable not set')

            client = OpenAI(api_key=api_key)
            prompt = self._build_prompt(query, contexts)
            try:
                # Use the new OpenAI client API
                resp = client.chat.completions.create(
                    model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.0,
                )
                # extract text from response
                return resp.choices[0].message.content
            except Exception as e:
                logger.exception('OpenAI request failed: %s', e)
                return "The external model failed; please try again later."

        raise NotImplementedError(f"Unknown generator mode: {self.mode}")

