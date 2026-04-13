import os
from unittest.mock import Mock, patch, MagicMock
from src.generator import Generator


def test_openai_generator_mocked():
    # Provide a fake API key so the generator doesn't fail on env check
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test'}):
        # Mock the OpenAI client and response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = 'Mocked openai response'

        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.chat.completions.create.return_value = mock_response

            gen = Generator(mode='openai')
            res = gen.generate('What is AI?', [('doc1.txt', 'AI stands for artificial intelligence.', 0.9)])
            assert 'Mocked openai response' in res
