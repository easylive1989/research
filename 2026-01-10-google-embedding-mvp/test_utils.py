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

    @patch('utils.chromadb')
    def test_chroma_integration(self, mock_chromadb):
        # Setup mock
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Test initialization
        collection = utils.get_chroma_collection()
        mock_chromadb.PersistentClient.assert_called()
        mock_client.get_or_create_collection.assert_called_with(name="embeddings_store")

        # Test save
        text = "sample text"
        embedding = [0.1, 0.2]
        metadata = {"source": "test.txt"}

        doc_id = utils.save_to_chroma(collection, text, embedding, metadata)

        mock_collection.add.assert_called()
        # Verify call arguments
        args = mock_collection.add.call_args
        self.assertEqual(args.kwargs['documents'], [text])
        self.assertEqual(args.kwargs['embeddings'], [embedding])
        self.assertEqual(args.kwargs['metadatas'], [metadata])

if __name__ == '__main__':
    unittest.main()
