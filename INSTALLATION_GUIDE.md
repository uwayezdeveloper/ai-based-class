# Installation Guide - AI-Based Learning Management System

## Prerequisites

Before installing the project, ensure you have the following installed on your computer:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **XAMPP (for MySQL database)**
   - Download from: https://www.apachefriends.org/
   - Or install MySQL separately

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads/

## Installation Steps

### Step 1: Download/Clone the Project

**Option A: Clone from GitHub**
```bash
git clone https://github.com/uwayezdeveloper/ai-based-class.git
cd ai-based-class
```

**Option B: Copy Files Manually**
- Copy the entire project folder to your desired location
- Navigate to the project directory

### Step 2: Set Up Python Virtual Environment

Open Command Prompt/Terminal in the project directory:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

With the virtual environment activated:
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install flask flask-cors mysql-connector-python werkzeug PyPDF2 sentence-transformers google-generativeai
```

### Step 4: Set Up MySQL Database

1. **Start XAMPP**
   - Open XAMPP Control Panel
   - Start Apache and MySQL services

2. **Create Database**
   - Open phpMyAdmin: http://localhost/phpmyadmin
   - Or use MySQL command line:
   ```sql
   mysql -u root -p
   CREATE DATABASE ai_lms;
   ```

### Step 5: Configure Database Connection

1. Open `config/database.py`
2. Update database credentials if needed:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password if any
    'database': 'ai_lms'
}
```

### Step 6: Configure Gemini AI API Key

1. Get your API key from: https://makersuite.google.com/app/apikey
2. Open `services/ai_chatbot.py`
3. Add your API key:
```python
genai.configure(api_key='YOUR_API_KEY_HERE')
```

### Step 7: Run Database Migration

The database tables will be created automatically on first run, but you may need to run the quiz submissions migration:

```bash
python migrate_quiz_submissions.py
```

### Step 8: Create Upload Directories

The app will create these automatically, but you can create them manually:
```bash
mkdir uploads
mkdir uploads\pdfs
```

**On Mac/Linux:**
```bash
mkdir -p uploads/pdfs
```

### Step 9: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

### Step 10: Access the System

#### Default Login Credentials:

**Admin:**
- Email: `admin@example.com`
- Password: `admin123`

**HOD (Head of Department):**
- Email: `hod@example.com`
- Password: `hod123`

**Lecturer:**
- Email: `lecturer1@example.com`
- Password: `lecturer123`

**Student:**
- Email: `student@example.com`
- Password: `student123`

## Project Structure

```
ai-based-class/
├── app.py                      # Main application file
├── config/
│   └── database.py             # Database configuration
├── services/
│   ├── ai_chatbot.py           # Gemini AI chatbot service
│   └── pdf_processor.py        # PDF processing for RAG
├── templates/                  # HTML templates
│   ├── admin/                  # Admin templates
│   ├── hod/                    # HOD templates
│   ├── lecturer/               # Lecturer templates
│   └── student/                # Student templates
├── static/                     # CSS, JS, images
├── uploads/                    # Uploaded materials
│   └── pdfs/                   # PDF files
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Troubleshooting

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to any available port
```

### Issue: MySQL connection error
**Solutions:**
- Ensure MySQL is running in XAMPP
- Check database credentials in `config/database.py`
- Verify database `ai_lms` exists

### Issue: Import errors
**Solution:** Make sure virtual environment is activated and all dependencies are installed:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Gemini AI not working
**Solutions:**
- Verify your API key is correct in `services/ai_chatbot.py`
- Check internet connection
- Ensure you have API quota available

### Issue: File upload errors
**Solution:** Ensure the `uploads/pdfs` directory exists and has write permissions

### Issue: Missing database columns
**Solution:** Run the migration script:
```bash
python migrate_quiz_submissions.py
```

## Additional Configuration

### Email Configuration (Optional)
To enable email notifications, update email settings in `app.py`

### Security (Production)
For production deployment:
1. Set `debug=False` in `app.py`
2. Use strong passwords for all default accounts
3. Enable HTTPS
4. Set up proper firewall rules
5. Use environment variables for sensitive data

## System Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 4GB
- Storage: 2GB free space
- OS: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)

**Recommended:**
- CPU: Quad-core processor
- RAM: 8GB
- Storage: 5GB free space
- Internet connection for AI features

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the error logs in the terminal
- Contact: uwayezdeveloper@gmail.com

## Features

- **Role-Based Access Control**: Admin, HOD, Lecturer, Student
- **Course Management**: Create and manage courses
- **Learning Materials**: Upload and share PDF materials
- **Quiz System**: Create quizzes with multiple question types
- **Auto & Manual Marking**: Automated grading with manual review
- **AI Chatbot**: Context-aware chatbot using Gemini AI
- **Reports**: Generate and download quiz reports
- **Lecturer Management**: HOD can assign courses to lecturers

## License

This project is for educational purposes.
