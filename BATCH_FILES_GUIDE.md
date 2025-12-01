# Quick Start Guide

## 🚀 First Time Setup

### Option 1: Automatic Setup (Recommended)
**Double-click:** `start.bat`

This will automatically:
- Check for virtual environment
- Run setup if needed
- Check if MySQL is running
- Start the application

### Option 2: Manual Setup
1. **Double-click:** `setup.bat`
   - Creates virtual environment
   - Installs all dependencies
   - Initializes database
   - Creates default users

2. **Double-click:** `start.bat` or `run.bat`
   - Starts the application

---

## 📝 Batch Files Explained

### `setup.bat` - First Time Installation
Run this **once** before using the system for the first time.

**What it does:**
1. ✅ Checks if Python is installed
2. ✅ Creates virtual environment (venv)
3. ✅ Installs all Python packages from requirements.txt
4. ✅ Creates upload directories
5. ✅ Checks if MySQL is running
6. ✅ Initializes database and creates tables
7. ✅ Updates database schema with new features
8. ✅ Verifies installation

**Requirements:**
- Python 3.8+ installed
- XAMPP MySQL running

---

### `start.bat` - Quick Start (Recommended)
Use this to **start the application** every time.

**What it does:**
1. ✅ Checks if setup has been run (venv exists)
2. ✅ Runs setup.bat automatically if needed
3. ✅ Checks if MySQL is running
4. ✅ Activates virtual environment
5. ✅ Starts the Flask application

**Best for:** Daily use - just double-click and go!

---

### `run.bat` - Simple Start
Alternative way to **start the application**.

**What it does:**
1. ✅ Checks if MySQL is running
2. ✅ Activates virtual environment
3. ✅ Starts the Flask application

**Best for:** When you know setup is already done and just want to run the app quickly.

---

## 🔑 Default Login Credentials

After setup completes, use these credentials:

**Admin Account:**
- Email: `admin@example.com`
- Password: `admin123`

**HOD Account:**
- Email: `hod@example.com`
- Password: `hod123`

**Students:** Register through the registration page

---

## 🌐 Access the Application

Once started, open your browser and go to:
- **http://localhost:5000**
- **http://127.0.0.1:5000**

---

## ⚠️ Troubleshooting

### "MySQL is not running" error
**Solution:**
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait for it to turn green
4. Run the batch file again

### "Virtual environment not found" error
**Solution:**
- Run `setup.bat` first

### "Failed to install dependencies" error
**Solution:**
- Make sure you have internet connection
- Run as Administrator (right-click → Run as administrator)
- Check if Python is properly installed: `python --version`

### Port already in use (5000)
**Solution:**
- Stop any other Flask applications
- Or edit `app.py` and change the port number

---

## 📁 Project Structure

```
clement/
├── setup.bat          ← First time setup (run once)
├── start.bat          ← Quick start (recommended)
├── run.bat            ← Simple start (alternative)
├── app.py             ← Main application file
├── requirements.txt   ← Python dependencies
├── venv/              ← Virtual environment (created by setup)
├── config/
│   └── database.py    ← Database initialization
├── services/
│   ├── ai_chatbot.py  ← Gemini AI chatbot
│   └── pdf_processor.py
├── templates/         ← HTML templates
└── uploads/           ← PDF uploads folder
```

---

## 🎯 Typical Workflow

### First Time:
```
1. Double-click: setup.bat
   (Wait for completion)

2. Double-click: start.bat
   (Application starts)

3. Open browser: http://localhost:5000

4. Login with admin credentials
```

### Daily Use:
```
1. Make sure XAMPP MySQL is running

2. Double-click: start.bat

3. Open browser: http://localhost:5000
```

---

## 🛠️ Manual Commands (If needed)

If you prefer command line:

```powershell
# First time setup
.\setup.bat

# Start application
.\start.bat

# OR manually:
.\venv\Scripts\Activate.ps1
python app.py
```

---

## ✅ Success Indicators

When everything works correctly, you should see:

```
================================================
Starting AI-Powered Learning Management System
================================================

Access the system at: http://localhost:5000

Default Login:
  Admin: admin@example.com / admin123
  HOD: hod@example.com / hod123

Press Ctrl+C to stop the server

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🎉 You're All Set!

The system is now ready to use. Enjoy your AI-Powered Learning Management System!
