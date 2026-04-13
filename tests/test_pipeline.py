from src.system import QAPipeline

def test_pipeline(tmp_path):
    docs = tmp_path / 'docs'
    docs.mkdir()
    (docs / 'doc1.txt').write_text('Python is a programming language used for automation and data analysis')
    p = QAPipeline(docs_dir=str(docs), generator_mode='mock')
    r = p.answer('what is Python used for?')
    assert 'answer' in r
    assert 0.0 <= r['confidence'] <= 1.0
