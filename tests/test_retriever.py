from src.retriever import SimpleRetriever
import os

def test_retriever_basic(tmp_path):
    docs = tmp_path / 'docs'
    docs.mkdir()
    (docs / 'a.txt').write_text('apples are tasty and red')
    (docs / 'b.txt').write_text('oranges are citrus fruits')
    r = SimpleRetriever(str(docs))
    r.load_documents()
    r.fit()
    res = r.retrieve('apples', top_k=1)
    assert len(res) == 1
    assert 'a.txt' in res[0][0]
