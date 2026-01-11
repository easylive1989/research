import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set it in a .env file or your environment.")
        return

    try:
        genai.configure(api_key=api_key)

        # Use the embedding model
        model = 'models/text-embedding-004'
        text_to_embed = "Hello, world! This is a Google Embedding MVP."

        print(f"Generating embedding for: '{text_to_embed}'")
        result = genai.embed_content(
            model=model,
            content=text_to_embed,
            task_type="RETRIEVAL_DOCUMENT",
            title="Embedding of single string"
        )

        embedding = result['embedding']
        print(f"Embedding generated successfully!")
        print(f"Dimension: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
