# Gemini AI Integration Setup Guide

## Overview
The AI-Powered LMS now includes Google Gemini AI integration for enhanced chatbot capabilities. The chatbot will:
- Read all uploaded PDF course materials
- Use Gemini AI to provide intelligent, context-aware responses
- Explain concepts clearly with additional educational insights
- Provide helpful answers even when no course materials are available

## Getting Your Gemini API Key

### Step 1: Visit Google AI Studio
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account

### Step 2: Create API Key
1. Click **"Get API Key"** or **"Create API Key"**
2. Select **"Create API key in new project"** (or use existing project)
3. Copy the generated API key

### Step 3: Configure the Application
1. Open the file: `C:\xampp\htdocs\clement\.env`
2. Find the line: `GEMINI_API_KEY=your-gemini-api-key-here`
3. Replace `your-gemini-api-key-here` with your actual API key
4. Save the file

Example:
```env
GEMINI_API_KEY=AIzaSyAbCdEf1234567890GhIjKlMnOpQrStUvWx
```

### Step 4: Restart the Application
1. Stop the running Flask application (Ctrl+C in terminal)
2. Run: `python app.py`

## Features

### With Gemini API (Recommended)
✅ Intelligent responses using advanced AI
✅ Reads and understands all uploaded course materials
✅ Provides detailed explanations with examples
✅ Answers general educational questions
✅ Contextual understanding across multiple documents

### Without Gemini API (Fallback Mode)
✅ Basic responses using local processing
✅ Extracts information from uploaded PDFs
✅ Simple keyword-based responses
⚠️ Limited understanding and context

## Testing the Chatbot

1. Login as a **student** account:
   - Email: `student@gmail.com`
   - Password: `student@gmail.com`

2. Navigate to **AI Chatbot** from the sidebar

3. Ask questions like:
   - "What is covered in this course?"
   - "Explain [topic from PDF materials]"
   - "Can you summarize the key points?"
   - "Help me understand [specific concept]"

## How It Works

1. **Student asks a question** → System searches uploaded PDFs for relevant content
2. **PDF content extracted** → Most relevant sections are identified using semantic search
3. **Gemini AI processes** → Question + PDF context sent to Gemini
4. **Intelligent response** → Gemini provides educational answer combining course materials and its knowledge
5. **Response displayed** → Student sees comprehensive, helpful answer

## Troubleshooting

### "Gemini API key not found" or responses seem basic
- Check that you've added your API key to `.env` file
- Ensure the API key is valid (test at Google AI Studio)
- Restart the Flask application

### API Key Errors
- Verify the API key is correctly copied (no extra spaces)
- Check if your Google account has API access enabled
- Ensure you're using Gemini Pro (not other models)

### No Course Materials Found
- HOD must upload PDF course materials first
- PDFs need to be processed (happens automatically on upload)
- Make sure the student is enrolled in courses with uploaded materials

## API Limits (Free Tier)

Google Gemini Free Tier includes:
- **60 requests per minute**
- **1,500 requests per day**
- Sufficient for typical classroom usage

If you exceed limits, the system automatically falls back to local processing.

## Privacy & Data

- Student questions and course materials are sent to Google Gemini API
- Google's privacy policy applies: https://ai.google.dev/terms
- Chat history is stored in your local database only
- No data is stored by Google beyond the API call

## Optional: Disable Gemini AI

If you prefer to use only local processing:
1. Don't add an API key to `.env`
2. Or set: `GEMINI_API_KEY=`
3. The system will automatically use local fallback mode

---

**Need Help?** Check the API key is correct and the application has been restarted!
