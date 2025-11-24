# AI-Powered Learning Management System - Quick Start Guide

## 🚀 Quick Setup (3 Steps)

### 1️⃣ Start MySQL
- Open XAMPP Control Panel
- Click "Start" for MySQL

### 2️⃣ Install Dependencies
Double-click `setup.bat` (This will create venv and install packages)
Or manually run:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Run the Application
Double-click `run.bat` (This will activate venv and run app)
Or manually run:
```powershell
venv\Scripts\activate
python app.py
```

## 🌐 Access the System
Open your browser and go to: **http://localhost:5000**

## 🔑 Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@gmail.com | admin@gmail.com |
| **HOD** | hod@gmail.com | hod@gmail.com |
| **Student** | student@gmail.com | student@gmail.com |

## 📋 System Workflow

### Admin Workflow:
1. Login with admin credentials
2. Create departments (e.g., Computer Science, Mathematics)
3. Add HODs and assign them to departments

### HOD Workflow:
1. Login with HOD credentials
2. Add courses to your assigned department
3. Upload PDF materials for each course
4. Create quizzes for students

### Student Workflow:
1. Register a new account or login
2. Select a department to study
3. Browse courses and read PDF materials
4. Take quizzes and get instant feedback
5. Chat with AI assistant for help

## 🤖 AI Chatbot Features

The AI chatbot:
- ✅ Learns from uploaded PDF course materials
- ✅ Provides context-aware answers
- ✅ Uses online AI models for enhanced responses
- ✅ Works offline with fallback responses

## ⚙️ Configuration

### Database Settings
Edit `config/database.py` if needed:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'database': 'ai_lms'
}
```

### Virtual Environment
The system uses a Python virtual environment (venv):
- Created automatically by setup.bat
- Activated automatically by run.bat
- Keeps dependencies isolated

## 🛠️ Troubleshooting

**Problem:** Port 5000 is already in use
**Solution:** Change port in `app.py` line 665:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Problem:** MySQL connection error
**Solution:** 
- Ensure XAMPP MySQL is running
- Check credentials in `config/database.py`

**Problem:** AI models not downloading
**Solution:**
- Ensure internet connection
- Models (~400MB) download on first run
- Be patient during first startup

## 📦 What's Included

- ✅ User management (Admin, HOD, Student)
- ✅ Department & Course management
- ✅ PDF upload and viewing
- ✅ Quiz creation and auto-grading
- ✅ AI chatbot with RAG
- ✅ Responsive web interface
- ✅ Automatic database initialization

## 🔒 Security Note

⚠️ **Before deploying to production:**
1. Change secret key in `app.py`
2. Update default passwords
3. Enable HTTPS
4. Set debug=False

## 📞 Need Help?

Check the full **README.md** for detailed documentation.

---

**Version:** 1.0.0  
**Built with:** Flask, MySQL, AI/ML  
**License:** Educational Use
