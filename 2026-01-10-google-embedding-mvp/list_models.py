import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    for m in genai.list_models():
        if 'embed' in m.name:
            print(f"- {m.name}: {m.supported_generation_methods}")
else:
    print("No API key found.")
