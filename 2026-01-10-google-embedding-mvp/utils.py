import google.generativeai as genai
from pypdf import PdfReader
from PIL import Image
import chromadb
import uuid
import os

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream.
    """
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

def get_image_description(image_file, api_key):
    """
    Generates a description for an image using Gemini 1.5 Flash.
    """
    try:
        genai.configure(api_key=api_key)
        # Use a vision-capable model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Open the image using Pillow
        image = Image.open(image_file)

        prompt = "Describe this image in detail for the purpose of generating a semantic text embedding. Focus on the main subjects, context, and visual elements."

        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        raise Exception(f"Error processing image: {e}")

def get_embedding(text, api_key, model_name='models/text-embedding-004'):
    """
    Generates an embedding for the given text.
    """
    try:
        genai.configure(api_key=api_key)
        result = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT",
            title="Uploaded File Content"
        )
        return result['embedding']
    except Exception as e:
        raise Exception(f"Error generating embedding: {e}")

def get_chroma_collection(path="./chroma_db", collection_name="embeddings_store"):
    """
    Initializes and returns a ChromaDB collection.
    """
    try:
        client = chromadb.PersistentClient(path=path)
        collection = client.get_or_create_collection(name=collection_name)
        return collection
    except Exception as e:
        raise Exception(f"Error initializing ChromaDB: {e}")

def save_to_chroma(collection, text, embedding, metadata=None):
    """
    Saves text, embedding, and metadata to ChromaDB.
    """
    try:
        doc_id = str(uuid.uuid4())
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id]
        )
        return doc_id
    except Exception as e:
        raise Exception(f"Error saving to ChromaDB: {e}")
