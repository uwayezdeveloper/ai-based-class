# AI-LMS User Roles and SQL Setup Guide

## 📋 System Roles Overview

### 1. **ADMIN** (System Administrator)
- **Access Level:** Full system access
- **Capabilities:**
  - Manage all departments
  - Manage all users (HODs, Lecturers, Students)
  - System configuration
  - View all reports

### 2. **HOD** (Head of Department)
- **Access Level:** Department-level management
- **Capabilities:**
  - Manage lecturers in their department
  - Create and assign courses to lecturers
  - Delete courses
  - View department courses and materials
  - Generate reports (quiz attendance, student performance)
  - Download reports as PDF
  - Cannot create quizzes or upload materials (lecturer responsibility)

### 3. **LECTURER** (Course Instructor)
- **Access Level:** Assigned courses only
- **Capabilities:**
  - View assigned courses
  - Upload learning materials (PDFs)
  - Create quizzes for assigned courses
  - Mark quizzes (auto-marking + manual marking)
  - View student submissions
  - Manage course content
  - Cannot assign courses to other lecturers

### 4. **STUDENT** (Learner)
- **Access Level:** Enrolled courses
- **Capabilities:**
  - Select department
  - View courses in their department
  - Download learning materials
  - Take quizzes
  - View quiz results
  - Use AI chatbot for learning assistance
  - Cannot create or manage content

---

## 🗄️ Database Structure

### Core Tables

#### 1. **users** - All system users
```sql
- id (Primary Key)
- name
- email (Unique)
- password (Hashed)
- role (ENUM: 'admin', 'hod', 'lecturer', 'student')
- department_id (Foreign Key to departments)
- created_at
- updated_at
```

#### 2. **departments** - Academic departments
```sql
- id (Primary Key)
- name
- description
- created_at
- updated_at
```

#### 3. **courses** - Course catalog
```sql
- id (Primary Key)
- name
- code
- description
- department_id (Foreign Key)
- created_by (User ID)
- created_at
- updated_at
```

#### 4. **course_lecturers** - Lecturer-Course assignments (NEW)
```sql
- id (Primary Key)
- course_id (Foreign Key to courses)
- lecturer_id (Foreign Key to users)
- assigned_by (Foreign Key to users - HOD)
- assigned_at
- UNIQUE constraint: (course_id, lecturer_id)
```

#### 5. **materials** - Learning materials
```sql
- id (Primary Key)
- course_id (Foreign Key)
- title
- file_path
- uploaded_by (User ID - Lecturer)
- created_at
```

#### 6. **quizzes** - Quiz definitions
```sql
- id (Primary Key)
- course_id (Foreign Key)
- department_id (Foreign Key)
- title
- description
- questions (JSON)
- duration (Minutes)
- created_by (User ID - Lecturer)
- created_at
```

#### 7. **quiz_submissions** - Student quiz attempts
```sql
- id (Primary Key)
- quiz_id (Foreign Key)
- user_id (Foreign Key - Student)
- course_id (Foreign Key)
- answers (JSON)
- score (Total score)
- auto_score (Auto-marked score)
- manual_score (Manually marked score)
- marking_status ('pending' or 'completed')
- marked_by (User ID - Lecturer)
- marked_at
- feedback
- submitted_at
```

---

## 🔧 SQL Queries for Setup

### 1. Add Lecturer Role to Existing Database

```sql
-- Update users table to include lecturer role
ALTER TABLE users 
MODIFY COLUMN role ENUM('admin', 'hod', 'lecturer', 'student') 
NOT NULL DEFAULT 'student';
```

### 2. Create Course Lecturers Table

```sql
CREATE TABLE IF NOT EXISTS course_lecturers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    lecturer_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_course_lecturer (course_id, lecturer_id),
    INDEX idx_course (course_id),
    INDEX idx_lecturer (lecturer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3. Create Default Users

```sql
-- Admin User
INSERT INTO users (name, email, password, role) 
VALUES (
    'Admin User',
    'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5qlOthKUDfKyK', -- admin123
    'admin'
);

-- HOD User (requires department_id)
INSERT INTO users (name, email, password, role, department_id) 
VALUES (
    'HOD User',
    'hod@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5qlOthKUDfKyK', -- hod123
    'hod',
    1  -- Computer Science department
);

-- Lecturer Users
INSERT INTO users (name, email, password, role, department_id) 
VALUES 
    (
        'Dr. John Smith',
        'lecturer1@example.com',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5qlOthKUDfKyK', -- lecturer123
        'lecturer',
        1
    ),
    (
        'Prof. Sarah Johnson',
        'lecturer2@example.com',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5qlOthKUDfKyK', -- lecturer123
        'lecturer',
        1
    );
```

### 4. Assign Courses to Lecturers

```sql
-- Assign specific course to a lecturer
INSERT INTO course_lecturers (course_id, lecturer_id, assigned_by)
VALUES (
    1,  -- Course ID
    3,  -- Lecturer User ID
    2   -- HOD User ID who made the assignment
);

-- Auto-assign all courses to lecturers in same department
INSERT INTO course_lecturers (course_id, lecturer_id, assigned_by)
SELECT 
    c.id, 
    u.id, 
    (SELECT id FROM users WHERE role='hod' AND department_id = c.department_id LIMIT 1)
FROM courses c
CROSS JOIN users u
WHERE u.role = 'lecturer' 
AND u.department_id = c.department_id
AND NOT EXISTS (
    SELECT 1 FROM course_lecturers cl 
    WHERE cl.course_id = c.id AND cl.lecturer_id = u.id
);
```

### 5. Update Existing Users' Roles

```sql
-- Set specific user as admin
UPDATE users SET role = 'admin' 
WHERE email = 'admin@example.com';

-- Set specific users as HODs
UPDATE users SET role = 'hod' 
WHERE email IN ('hod@example.com', 'hod1@example.com');

-- Set specific users as lecturers
UPDATE users SET role = 'lecturer' 
WHERE email IN ('lecturer1@example.com', 'lecturer2@example.com');

-- Set all others as students (if needed)
UPDATE users SET role = 'student' 
WHERE role NOT IN ('admin', 'hod', 'lecturer');
```

---

## 🚀 Setup Instructions

### Option 1: Automated Setup (Recommended)

```powershell
# Run the migration script
python migrate_lecturer_role.py
```

### Option 2: Manual SQL Setup

1. Open phpMyAdmin or MySQL command line
2. Select the `ai_lms` database
3. Run the SQL queries from `migrate_lecturer_role.sql`

### Option 3: Fresh Installation

```powershell
# Initialize database from scratch
python config/database.py
```

---

## 🔑 Default Login Credentials

After setup, use these credentials:

| Role      | Email                    | Password     | Access Level                          |
|-----------|--------------------------|--------------|---------------------------------------|
| Admin     | admin@example.com        | admin123     | Full system access                    |
| HOD       | hod@example.com          | hod123       | Department management, lecturer mgmt  |
| Lecturer  | lecturer1@example.com    | lecturer123  | Assigned courses only                 |
| Lecturer  | lecturer2@example.com    | lecturer123  | Assigned courses only                 |
| Lecturer  | lecturer3@example.com    | lecturer123  | Assigned courses only                 |
| Student   | (Register via website)   | -            | Course access, quizzes, chatbot       |

---

## 📊 Verification Queries

### Check User Roles

```sql
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role 
ORDER BY FIELD(role, 'admin', 'hod', 'lecturer', 'student');
```

### View All Users with Roles

```sql
SELECT id, name, email, role, department_id
FROM users
ORDER BY FIELD(role, 'admin', 'hod', 'lecturer', 'student'), name;
```

### View Course Assignments

```sql
SELECT 
    c.name as course_name,
    c.code as course_code,
    u.name as lecturer_name,
    u.email as lecturer_email,
    d.name as department_name,
    cl.assigned_at
FROM course_lecturers cl
JOIN courses c ON cl.course_id = c.id
JOIN users u ON cl.lecturer_id = u.id
JOIN departments d ON c.department_id = d.id
ORDER BY d.name, c.name;
```

### Find Lecturers Without Courses

```sql
SELECT u.name, u.email, d.name as department
FROM users u
LEFT JOIN course_lecturers cl ON u.id = cl.lecturer_id
LEFT JOIN departments d ON u.department_id = d.id
WHERE u.role = 'lecturer' AND cl.id IS NULL;
```

### Find Courses Without Lecturers

```sql
SELECT c.name, c.code, d.name as department
FROM courses c
LEFT JOIN course_lecturers cl ON c.id = cl.course_id
LEFT JOIN departments d ON c.department_id = d.id
WHERE cl.id IS NULL;
```

---

## 🎯 Workflow Examples

### HOD Workflow

1. Login as HOD
2. Go to "Manage Lecturers"
3. Add new lecturer (or view existing)
4. Go to "Manage Courses"
5. Create new course
6. Assign course to lecturer
7. Go to "Reports" to view quiz attendance and performance

### Lecturer Workflow

1. Login as lecturer
2. View "My Courses" (assigned courses only)
3. Select a course
4. Upload PDF materials
5. Create quizzes
6. View student submissions
7. Mark quizzes (manual marking for open-ended questions)

### Student Workflow

1. Register and login
2. Select department
3. View available courses
4. Download materials
5. Take quizzes
6. Use AI chatbot for help
7. View quiz results

---

## 🔄 Migration Notes

- The migration scripts are **safe to run multiple times**
- Existing data will not be deleted
- Default users will only be created if they don't exist
- Use `ON DUPLICATE KEY UPDATE` for idempotent operations

---

## ✅ Post-Setup Checklist

- [ ] Database tables created successfully
- [ ] All 4 roles present in users table
- [ ] course_lecturers table created
- [ ] Default admin account created
- [ ] Default HOD account created
- [ ] Default lecturer accounts created
- [ ] Can login with each role
- [ ] HOD can assign courses to lecturers
- [ ] Lecturers can see assigned courses only
- [ ] Students can register and enroll

---

For any issues, run:
```powershell
python verify_installation.py
```
