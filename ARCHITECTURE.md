# System Architecture & User Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI-Powered LMS                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │  Admin   │      │   HOD    │      │ Student  │          │
│  └────┬─────┘      └────┬─────┘      └────┬─────┘          │
│       │                 │                  │                 │
│       └─────────────────┴──────────────────┘                │
│                         │                                    │
│                    ┌────▼────┐                              │
│                    │  Flask  │                              │
│                    │  Routes │                              │
│                    └────┬────┘                              │
│                         │                                    │
│       ┌─────────────────┼─────────────────┐                │
│       │                 │                 │                 │
│  ┌────▼────┐      ┌────▼────┐      ┌────▼────┐           │
│  │  MySQL  │      │   PDF   │      │   AI    │           │
│  │Database │      │Processor│      │Chatbot  │           │
│  └─────────┘      └─────────┘      └─────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## User Roles & Permissions

### 👨‍💼 Admin
```
Admin Dashboard
├── Manage Departments
│   ├── Create Department
│   ├── View All Departments
│   └── Edit Department Info
├── Manage HODs
│   ├── Add HOD
│   ├── Assign to Department
│   └── View All HODs
└── View System Statistics
```

### 👨‍🏫 HOD (Head of Department)
```
HOD Dashboard
├── Manage Courses
│   ├── Add Course
│   ├── Edit Course
│   └── Delete Course
├── Manage Materials
│   ├── Upload PDF Files
│   ├── View Materials
│   └── Delete Materials
└── Manage Quizzes
    ├── Create Quiz
    ├── Add Questions
    └── View Submissions
```

### 👨‍🎓 Student
```
Student Dashboard
├── Select Department
├── Browse Courses
├── View Materials
│   └── Read PDF Files
├── Take Quizzes
│   ├── Timed Assessment
│   ├── Auto Grading
│   └── View Results
└── AI Chatbot
    ├── Ask Questions
    ├── Get Help from PDFs
    └── Online AI Assistance
```

## Data Flow

### 1. PDF Upload & Processing Flow
```
HOD uploads PDF
    ↓
File saved to uploads/pdfs/
    ↓
PDF text extracted (PyPDF2)
    ↓
Text chunked into segments
    ↓
Embeddings generated (Sentence Transformers)
    ↓
Stored in pdf_embeddings table
    ↓
Available for AI Chatbot
```

### 2. Quiz Flow
```
HOD creates quiz
    ↓
Questions stored as JSON
    ↓
Student takes quiz
    ↓
Timer starts (auto-submit on timeout)
    ↓
Student submits answers
    ↓
Auto-grading (compare with correct answers)
    ↓
Score calculated and stored
    ↓
Results displayed immediately
```

### 3. AI Chatbot Flow
```
Student asks question
    ↓
Query embedding generated
    ↓
Search similar chunks in PDF embeddings
    ↓
Retrieve relevant context from PDFs
    ↓
Send to AI model (Hugging Face API)
    ↓
Generate response with context
    ↓
Display to student
```

## Database Schema

### Tables
1. **users** - All system users (admin, hod, student)
2. **departments** - Academic departments
3. **courses** - Courses per department
4. **materials** - PDF materials per course
5. **quizzes** - Quiz data with questions (JSON)
6. **quiz_submissions** - Student quiz attempts and scores
7. **chat_history** - AI chatbot conversation logs
8. **pdf_embeddings** - Vector embeddings for AI RAG

## Technology Stack Details

### Backend
- **Flask 3.0.0** - Web framework
- **MySQL** - Database
- **Werkzeug** - Security (password hashing)
- **Flask-CORS** - Cross-origin support

### AI/ML
- **Sentence Transformers** - Text embeddings
- **PyPDF2** - PDF text extraction
- **Hugging Face API** - Online AI models
- **NumPy** - Vector operations

### Frontend
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **JavaScript/jQuery** - Interactivity

## Security Features

1. **Password Hashing** - Werkzeug security
2. **Session Management** - Flask sessions
3. **Role-Based Access Control** - Decorators
4. **File Upload Validation** - PDF only, size limits
5. **SQL Injection Prevention** - Parameterized queries

## Deployment Checklist

- [ ] Change SECRET_KEY in app.py
- [ ] Update default passwords
- [ ] Set DEBUG=False
- [ ] Configure MySQL with strong password
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Set up backup system
- [ ] Configure logging
- [ ] Add monitoring
- [ ] Test all features

## Performance Optimization

### Recommended for Production:
1. Use Redis for session storage
2. Implement caching for embeddings
3. Use CDN for static files
4. Optimize PDF processing (async)
5. Add database indexing
6. Implement pagination
7. Use gunicorn/uwsgi instead of Flask dev server

## Future Enhancements

- [ ] Video content support
- [ ] Real-time notifications
- [ ] Discussion forums
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Integration with external LMS
- [ ] Certificate generation
- [ ] Payment integration
- [ ] Live classes support
