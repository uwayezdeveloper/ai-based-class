"""
Test script to verify Gemini AI integration
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini():
    print("=" * 60)
    print("Testing Gemini AI Integration")
    print("=" * 60)
    
    # Check if API key is loaded
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"✓ API Key loaded: {api_key[:20]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✓ Gemini model initialized")
        
        # Test with a simple question
        print("\nTesting with question: 'What is artificial intelligence?'")
        response = model.generate_content("What is artificial intelligence? Give a brief answer in 2-3 sentences.")
        
        if response and response.text:
            print("\n✓ Gemini Response:")
            print("-" * 60)
            print(response.text)
            print("-" * 60)
            print("\n✅ Gemini AI is working correctly!")
            return True
        else:
            print("❌ No response received from Gemini")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini()
