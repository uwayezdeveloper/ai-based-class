# Batch Scripts Guide - AI-Based LMS

## Available Scripts

This project includes several batch scripts to make setup and running easier on Windows.

### 🔧 setup.bat - Initial Setup
**Run this FIRST** when setting up the project for the first time.

**What it does:**
- Checks if Python is installed
- Creates virtual environment (venv)
- Installs all required Python packages
- Creates upload directories
- Verifies MySQL connection
- Shows setup instructions

**How to use:**
```bash
setup.bat
```

**When to use:**
- First time installing the project
- After downloading/cloning the project
- When dependencies need to be reinstalled

---

### ▶️ start.bat - Start Application (Recommended)
**Use this to start the application** after initial setup.

**What it does:**
- Activates virtual environment
- Checks MySQL connection
- Starts Flask application
- Shows login credentials
- Displays access URL

**How to use:**
```bash
start.bat
```

**Access application at:** http://localhost:5000

**Default credentials:**
- Admin: `admin@example.com` / `admin123`
- HOD: `hod@example.com` / `hod123`
- Lecturer: `lecturer1@example.com` / `lecturer123`
- Student: `student@example.com` / `student123`

---

### ⚡ run.bat - Quick Run
**Quick start** without checks (faster, use after everything is working).

**What it does:**
- Activates virtual environment
- Starts Flask application immediately

**How to use:**
```bash
run.bat
```

**When to use:**
- After initial setup is complete
- When you know MySQL is already running
- For quick development starts

---

### 🗄️ migrate.bat - Database Migration
**Run this to update database schema** (for quiz_submissions table).

**What it does:**
- Activates virtual environment
- Runs database migration script
- Adds missing columns to quiz_submissions table

**How to use:**
```bash
migrate.bat
```

**When to use:**
- After fresh database setup
- When database schema needs updating
- If you get "Unknown column" errors

---

### ⏹️ stop.bat - Stop Application
**Stop the running Flask application.**

**What it does:**
- Terminates all Python processes
- Stops the Flask server

**How to use:**
```bash
stop.bat
```

**Alternative:**
- Press `Ctrl+C` in the command window where app is running

---

## Quick Start Guide

### For First Time Setup:

1. **Install XAMPP** (if not already installed)
   - Download from: https://www.apachefriends.org/
   - Start Apache and MySQL services

2. **Create Database**
   - Open phpMyAdmin: http://localhost/phpmyadmin
   - Create database: `ai_lms`
   ```sql
   CREATE DATABASE ai_lms;
   ```

3. **Run Setup**
   ```bash
   setup.bat
   ```

4. **Configure Gemini AI** (Optional but recommended)
   - Get API key: https://makersuite.google.com/app/apikey
   - Edit `services/ai_chatbot.py`
   - Add your API key

5. **Run Migration**
   ```bash
   migrate.bat
   ```

6. **Start Application**
   ```bash
   start.bat
   ```

7. **Access System**
   - Open browser: http://localhost:5000
   - Login with default credentials

---

## Daily Usage Workflow

### Starting Work:
1. Start XAMPP (Apache + MySQL)
2. Run `start.bat` or `run.bat`
3. Open http://localhost:5000

### Stopping Work:
- Press `Ctrl+C` in terminal
- Or run `stop.bat`

---

## Troubleshooting

### Error: "Python is not installed"
**Solution:** Install Python from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### Error: "Cannot connect to MySQL"
**Solution:**
1. Open XAMPP Control Panel
2. Start MySQL service
3. Verify database `ai_lms` exists

### Error: "Virtual environment not found"
**Solution:** Run `setup.bat` first

### Error: "Unknown column in field list"
**Solution:** Run `migrate.bat`

### Port 5000 already in use
**Solution:** Edit `app.py` and change port:
```python
app.run(debug=True, port=5001)
```

---

## File Purposes

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `setup.bat` | Complete setup | First time only |
| `start.bat` | Start with checks | Regular use |
| `run.bat` | Quick start | Development |
| `migrate.bat` | Update database | After setup/updates |
| `stop.bat` | Stop server | End session |

---

## Tips

✅ **Always start XAMPP first** before running any script

✅ **Use start.bat for reliability** - it checks everything

✅ **Use run.bat for speed** - when you're sure everything works

✅ **Keep terminal open** to see error messages

✅ **Check localhost:5000** after starting to confirm it's running

---

## Common Commands

```bash
# First time setup
setup.bat

# Start application (recommended)
start.bat

# Quick start
run.bat

# Update database
migrate.bat

# Stop application
stop.bat
# OR press Ctrl+C

# Check if running
# Open: http://localhost:5000
```

---

## System Architecture

```
Project Root
├── app.py              # Main application
├── setup.bat           # Setup script
├── start.bat           # Start script  
├── run.bat             # Quick run script
├── migrate.bat         # Migration script
├── stop.bat            # Stop script
├── venv/               # Virtual environment (created by setup)
├── uploads/            # Uploaded files
│   └── pdfs/           # PDF materials
├── templates/          # HTML templates
├── services/           # Backend services
└── config/             # Configuration files
```

---

## Need Help?

1. Check error messages in terminal
2. Verify XAMPP/MySQL is running
3. Ensure database `ai_lms` exists
4. Try running `setup.bat` again
5. Check INSTALLATION_GUIDE.md for detailed steps

---

## Support

For issues or questions:
- Email: uwayezdeveloper@gmail.com
- Check: INSTALLATION_GUIDE.md
