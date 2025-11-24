# AI-Powered Learning Management System

A comprehensive Learning Management System with AI-powered chatbot capabilities built with Flask and MySQL.

## Features

### Admin Features
- Add and manage departments
- Add and manage HODs (Head of Departments)
- View system statistics

### HOD Features
- Add and manage courses in assigned department
- Upload course materials (PDF files)
- Create and manage quizzes
- Auto-process PDFs for AI chatbot

### Student Features
- Register and login to the system
- Select and change departments
- View and read course materials (PDFs)
- Take auto-graded quizzes
- Chat with AI assistant that learns from course materials
- Get instant answers from uploaded course PDFs and online resources

## Technology Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **AI/ML:** 
  - Sentence Transformers (for PDF embeddings)
  - Hugging Face Transformers (for chatbot)
  - RAG (Retrieval-Augmented Generation)
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **PDF Processing:** PyPDF2

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server (XAMPP or standalone)
- 4GB RAM minimum (for AI models)

### Step 1: Start MySQL Server
If using XAMPP:
1. Open XAMPP Control Panel
2. Start Apache and MySQL services

### Step 2: Setup Virtual Environment and Install Dependencies
```powershell
# Navigate to project directory
cd c:\xampp\htdocs\clement

# Run setup script (creates venv and installs packages)
setup.bat

# OR manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Initialize Database
The system will automatically create the database and tables on first run.
```powershell
python config/database.py
```

### Step 4: Run the Application
```powershell
# Using run script (recommended)
run.bat

# OR manually:
venv\Scripts\activate
python app.py
```

The application will be available at: http://localhost:5000

## Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@gmail.com | admin@gmail.com |
| HOD | hod@gmail.com | hod@gmail.com |
| Student | student@gmail.com | student@gmail.com |

## Database Configuration

To change database settings, edit `config/database.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change if you have a password
    'database': 'ai_lms'
}
```

## AI Chatbot Configuration

### Local AI Processing (No API Keys Required)
The system uses local AI processing with:
- `all-MiniLM-L6-v2` for text embeddings
- Intelligent context-based responses from uploaded PDFs
- No external API dependencies
- Works completely offline after initial model download

## Project Structure
```
clement/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── config/
│   ├── __init__.py
│   └── database.py            # Database configuration and initialization
├── services/
│   ├── __init__.py
│   ├── ai_chatbot.py          # AI chatbot logic
│   └── pdf_processor.py       # PDF processing and embeddings
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin/                 # Admin templates
│   ├── hod/                   # HOD templates
│   └── student/               # Student templates
└── uploads/                   # Uploaded files directory
    └── pdfs/                  # PDF storage
```

## Features in Detail

### AI Chatbot
- **RAG (Retrieval-Augmented Generation):** Retrieves relevant content from uploaded PDFs
- **Context-Aware:** Understands department-specific content
- **Online Integration:** Can access online AI models for enhanced responses
- **Fallback System:** Works offline with basic responses

### Quiz System
- Auto-grading functionality
- Timed quizzes
- Instant feedback
- Score tracking
- One submission per quiz

### PDF Management
- Upload and view PDFs
- Automatic text extraction
- Embedding generation for AI
- Department-specific organization

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL service is running in XAMPP
- Check database credentials in `config/database.py`

### AI Model Download Issues
- First run will download AI models (~400MB)
- Ensure stable internet connection
- Models are cached after first download

### PDF Upload Issues
- Check file size (max 50MB)
- Only PDF files are accepted
- Ensure `uploads/pdfs` directory exists

### Port Already in Use
If port 5000 is in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Security Notes

⚠️ **Important for Production:**
1. Change `app.secret_key` in `app.py`
2. Update default passwords
3. Enable HTTPS
4. Set `debug=False` in production
5. Use environment variables for sensitive data
6. Implement rate limiting
7. Add input validation and sanitization

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error logs in the terminal
3. Ensure all dependencies are installed

## License

This project is created for educational purposes.

## Version

1.0.0 - Initial Release

---

Built with ❤️ using Flask and AI
