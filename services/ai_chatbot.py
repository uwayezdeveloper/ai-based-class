import os
import google.generativeai as genai
from services.pdf_processor import PDFProcessor
from config.database import get_db_connection
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIChatbot:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            # Use Gemini 2.5 Flash - stable, fast, and versatile
            self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
            self.use_gemini = True
            print("✓ Gemini AI initialized successfully")
        else:
            self.use_gemini = False
            print("⚠ Warning: GEMINI_API_KEY not found in .env file")
    
    def get_context_from_pdfs(self, query, department_id=None):
        """Retrieve relevant context from uploaded PDFs (optional enhancement)"""
        try:
            similar_chunks = self.pdf_processor.search_similar_chunks(query, department_id, top_k=3)
            
            if not similar_chunks:
                return ""
            
            context = "Reference from course materials:\n\n"
            for idx, chunk in enumerate(similar_chunks, 1):
                context += f"{idx}. {chunk['chunk_text'][:500]}...\n\n"
            
            return context
        except Exception as e:
            print(f"Note: Could not retrieve PDF context: {e}")
            return ""  # Don't fail if PDFs aren't available
    
    def get_intelligent_response(self, query, context=""):
        """Get intelligent response using Gemini AI"""
        try:
            if not self.use_gemini:
                return self.get_fallback_response(query, context)
            
            # Build the prompt for Gemini
            if context:
                # If we have PDF context, include it as reference material
                prompt = f"""You are an intelligent learning assistant helping students understand their course materials.

Context from uploaded course materials:
{context}

Student's Question: {query}

Please provide a comprehensive and helpful answer. If the question is related to the course materials above, use that information. If the question is general or requires broader knowledge, provide a well-informed response using your knowledge. Always be educational, clear, and encouraging."""
            else:
                # No PDF context - answer from general knowledge
                prompt = f"""You are an intelligent learning assistant helping students with their studies.

Student's Question: {query}

Please provide a comprehensive, educational, and helpful answer. Be clear, encouraging, and thorough in your explanation. If it's a greeting or casual question, respond naturally. For academic questions, provide detailed explanations with examples where appropriate."""
            
            # Get response from Gemini
            response = self.gemini_model.generate_content(prompt)
            
            if response and response.text:
                return response.text
            else:
                return self.get_fallback_response(query, context)
                
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self.get_fallback_response(query, context)
    
    def get_fallback_response(self, query, context=""):
        """Provide a fallback response when Gemini is unavailable"""
        query_lower = query.lower()
        
        # Simple keyword-based responses for common queries
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your AI learning assistant powered by Gemini AI. I can help you with any questions - whether about your course materials or general knowledge. How can I assist you today?"
        
        elif any(word in query_lower for word in ['how are you', 'how do you do', 'whats up']):
            return "I'm doing great, thank you for asking! I'm here and ready to help you learn. What would you like to know about?"
        
        elif any(word in query_lower for word in ['help', 'what can you do', 'capabilities']):
            return (
                "I'm an AI learning assistant powered by Gemini AI. I can help you with:\n\n"
                "📚 Course Materials: Answer questions about uploaded PDFs and documents\n"
                "🎓 General Knowledge: Explain concepts, definitions, and academic topics\n"
                "💡 Learning Support: Help you understand complex subjects\n"
                "📝 Study Assistance: Provide summaries, examples, and clarifications\n"
                "🌐 Broad Topics: Answer questions on science, math, history, technology, and more\n\n"
                "Just ask me anything you'd like to learn about!"
            )
        
        elif any(word in query_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! I'm happy to help. Feel free to ask if you have more questions!"
        
        else:
            # If Gemini is not available, provide informative message
            if context:
                return (
                    f"I found some relevant information from your course materials:\n\n{context}\n\n"
                    "Note: Full AI capabilities are currently limited. Please check that the GEMINI_API_KEY "
                    "is properly configured in the .env file for enhanced responses."
                )
            else:
                return (
                    "I'd love to help you with that question! However, I'm currently running in limited mode. "
                    "To unlock my full AI capabilities:\n\n"
                    "1. Ensure the GEMINI_API_KEY is set in the .env file\n"
                    "2. Restart the application\n\n"
                    "Meanwhile, I can help if you have questions about uploaded course materials. "
                    "Make sure your HOD has uploaded relevant PDFs for your courses."
                )
    
    def get_response(self, query, department_id=None):
        """Main method to get chatbot response - Always uses Gemini AI"""
        try:
            # Get context from PDFs (optional, not required)
            context = self.get_context_from_pdfs(query, department_id)
            
            # ALWAYS use Gemini AI for intelligent responses
            # Whether we have PDF context or not, Gemini will provide the answer
            response = self.get_intelligent_response(query, context)
            
            return response
            
        except Exception as e:
            print(f"Error in chatbot response: {e}")
            return "I apologize, but I encountered an error processing your question. Please try again."
    
    def save_chat_history(self, user_id, message, response, department_id=None):
        """Save chat conversation to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO chat_history (user_id, message, response, department_id) VALUES (%s, %s, %s, %s)',
                (user_id, message, response, department_id)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def get_chat_history(self, user_id, limit=10):
        """Retrieve chat history for a user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                'SELECT message, response, created_at FROM chat_history WHERE user_id = %s ORDER BY created_at DESC LIMIT %s',
                (user_id, limit)
            )
            
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return list(reversed(history))
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []
