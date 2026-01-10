import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project directory to python path
sys.path.append(os.path.join(os.getcwd(), '2026-01-10-google-embedding-mvp'))

import utils

class TestUtils(unittest.TestCase):

    @patch('utils.genai')
    def test_get_embedding(self, mock_genai):
        # Setup mock
        mock_result = {'embedding': [0.1, 0.2, 0.3]}
        mock_genai.embed_content.return_value = mock_result

        # Test
        api_key = "dummy_key"
        text = "Hello world"
        embedding = utils.get_embedding(text, api_key)

        # Assert
        self.assertEqual(embedding, [0.1, 0.2, 0.3])
        mock_genai.configure.assert_called_with(api_key=api_key)
        mock_genai.embed_content.assert_called()

    @patch('utils.PdfReader')
    def test_extract_text_from_pdf(self, mock_pdf_reader):
        # Setup mock
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "PDF Page Content"

        mock_reader_instance = MagicMock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance

        # Test
        dummy_stream = MagicMock()
        text = utils.extract_text_from_pdf(dummy_stream)

        # Assert
        self.assertIn("PDF Page Content", text)

if __name__ == '__main__':
    unittest.main()
