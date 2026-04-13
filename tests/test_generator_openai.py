import os
from src.generator import Generator


def test_openai_generator_mocked(monkeypatch):
    # Provide a fake API key so the generator doesn't fail on env check
    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test')

    class DummyResp:
        def __init__(self):
            self.choices = [type('C', (), {'message': type('M', (), {'content': 'Mocked openai response'})})()]

    # monkeypatch the openai.ChatCompletion.create function
    import types
    dummy = DummyResp()

    def fake_create(*args, **kwargs):
        return dummy

    import sys
    import importlib
    # create a dummy openai module if not present
    if 'openai' not in sys.modules:
        import types as _types
        openai = _types.ModuleType('openai')
        sys.modules['openai'] = openai
        openai.ChatCompletion = types.SimpleNamespace(create=fake_create)
    else:
        import openai
        monkeypatch.setattr(openai.ChatCompletion, 'create', fake_create)

    gen = Generator(mode='openai')
    res = gen.generate('What is AI?', [('doc1.txt', 'AI stands for artificial intelligence.', 0.9)])
    assert 'Mocked openai response' in res
