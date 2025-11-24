"""
List available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    print("Available Gemini Models:")
    print("=" * 60)
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Description: {model.description}")
            print(f"  Supported methods: {model.supported_generation_methods}")
            print()
else:
    print("API key not found")
