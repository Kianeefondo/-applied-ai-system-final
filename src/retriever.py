import os
import math
from typing import List, Tuple
import numpy as np

class SimpleRetriever:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.docs = []  # list of (doc_id, text)
        self.vocab = {}
        self.doc_vectors = None
        self.idf = {}

    def load_documents(self):
        texts = []
        ids = []
        for fname in sorted(os.listdir(self.docs_dir)):
            if not fname.endswith('.txt'):
                continue
            path = os.path.join(self.docs_dir, fname)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            ids.append(fname)
            texts.append(text)
        self.docs = list(zip(ids, texts))
        return self.docs

    def fit(self):
        if not self.docs:
            self.load_documents()
        # build vocab
        vocab = {}
        doc_terms = []
        for (_, text) in self.docs:
            terms = [t.strip().lower() for t in text.split() if t.strip()]
            doc_terms.append(terms)
            for t in set(terms):
                vocab.setdefault(t, len(vocab))
        self.vocab = vocab
        # compute idf
        N = len(doc_terms)
        idf = {}
        for term, idx in vocab.items():
            df = sum(1 for terms in doc_terms if term in terms)
            idf[term] = math.log((1 + N) / (1 + df)) + 1.0
        self.idf = idf
        # compute tf-idf vectors
        vectors = np.zeros((N, len(vocab)), dtype=float)
        for i, terms in enumerate(doc_terms):
            tf = {}
            for t in terms:
                tf[t] = tf.get(t, 0) + 1
            for t, cnt in tf.items():
                vectors[i, vocab[t]] = (cnt / len(terms)) * idf[t]
        # normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vectors = vectors / norms
        self.doc_vectors = vectors

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
        if self.doc_vectors is None:
            self.fit()
        q_terms = [t.strip().lower() for t in query.split() if t.strip()]
        vec = np.zeros((len(self.vocab),), dtype=float)
        for t in q_terms:
            if t in self.vocab:
                vec[self.vocab[t]] += 1
        if vec.sum() == 0:
            # no overlap
            sims = np.zeros((self.doc_vectors.shape[0],), dtype=float)
        else:
            # apply idf
            for t, idx in self.vocab.items():
                vec[idx] *= self.idf.get(t, 1.0)
            norm = np.linalg.norm(vec)
            if norm == 0:
                sims = np.zeros((self.doc_vectors.shape[0],), dtype=float)
            else:
                vec = vec / norm
                sims = self.doc_vectors.dot(vec)
        # get top k
        idxs = np.argsort(sims)[::-1][:top_k]
        results = []
        for i in idxs:
            doc_id, text = self.docs[i]
            score = float(sims[i])
            results.append((doc_id, text, score))
        return results

