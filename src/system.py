import logging
from typing import Any, Dict
from .retriever import SimpleRetriever
from .generator import Generator

logger = logging.getLogger(__name__)

class QAPipeline:
    def __init__(self, docs_dir: str, generator_mode: str = 'mock'):
        self.retriever = SimpleRetriever(docs_dir)
        self.generator = Generator(generator_mode)

    def answer(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        logger.info('query=%s', query)
        contexts = self.retriever.retrieve(query, top_k=top_k)
        confidence = float(max((c[2] for c in contexts), default=0.0))
        answer = self.generator.generate(query, contexts)
        return {'query': query, 'answer': answer, 'confidence': confidence, 'retrieved': [{'doc_id': c[0], 'score': c[2]} for c in contexts]}
