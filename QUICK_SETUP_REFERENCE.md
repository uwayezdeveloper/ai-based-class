# Quick Setup Reference

## 🚀 First Time Setup

### Step 1: Run Migration
```powershell
python migrate_lecturer_role.py
```

### Step 2: Start Application
```powershell
python app.py
```

---

## 🔑 Default Credentials

| Role      | Email                  | Password     |
|-----------|------------------------|--------------|
| Admin     | admin@example.com      | admin123     |
| HOD       | hod@example.com        | hod123       |
| Lecturer  | lecturer1@example.com  | lecturer123  |
| Lecturer  | lecturer2@example.com  | lecturer123  |
| Lecturer  | lecturer3@example.com  | lecturer123  |

---

## 👥 Role Capabilities

### ADMIN
✅ Full system access
✅ Manage all users
✅ System configuration

### HOD (Head of Department)
✅ Add/manage lecturers
✅ Create courses
✅ Assign courses to lecturers
✅ Delete courses
✅ Generate reports (PDF download)
✅ View all department data
❌ Cannot create quizzes/upload materials

### LECTURER
✅ View assigned courses only
✅ Upload PDF materials
✅ Create quizzes
✅ Mark quizzes
✅ Manage course content
❌ Cannot assign courses
❌ Cannot access other courses

### STUDENT
✅ Select department
✅ View courses
✅ Download materials
✅ Take quizzes
✅ Use AI chatbot
✅ View results
❌ Cannot create content

---

## 🗄️ Database Tables

### New Table: `course_lecturers`
```sql
- course_id (Which course)
- lecturer_id (Which lecturer)
- assigned_by (HOD who assigned)
- assigned_at (When assigned)
```

### Updated: `users` table
```sql
role ENUM('admin', 'hod', 'lecturer', 'student')
```

---

## 📝 Key SQL Queries

### Add Lecturer Role
```sql
ALTER TABLE users 
MODIFY COLUMN role ENUM('admin', 'hod', 'lecturer', 'student');
```

### Create Course Assignment Table
```sql
CREATE TABLE course_lecturers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    lecturer_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY (course_id, lecturer_id)
);
```

### Assign Course to Lecturer
```sql
INSERT INTO course_lecturers (course_id, lecturer_id, assigned_by)
VALUES (1, 3, 2);
-- 1=course_id, 3=lecturer_id, 2=hod_id
```

---

## 🔄 Workflow

### HOD: Assign Course to Lecturer
1. Login as HOD
2. Menu → "Manage Lecturers"
3. Click "Add Lecturer" or view existing
4. Menu → "Manage Courses"
5. Create course → Select lecturer → Save
6. Lecturer now sees course in "My Courses"

### Lecturer: Manage Course
1. Login as lecturer
2. Menu → "My Courses"
3. Select assigned course
4. Upload materials / Create quiz
5. View submissions / Mark quizzes

### HOD: Generate Report
1. Login as HOD
2. Menu → "Reports"
3. Select quiz
4. View statistics
5. Click "Download PDF"

---

## ✅ Verification

```powershell
# Check all roles exist
python -c "from config.database import get_db_connection; conn = get_db_connection(); c = conn.cursor(); c.execute('SELECT DISTINCT role FROM users'); print(c.fetchall())"
```

Expected output:
```
[('admin',), ('hod',), ('lecturer',), ('student',)]
```

---

## 📁 Important Files

- `migrate_lecturer_role.py` - Migration script
- `migrate_lecturer_role.sql` - SQL queries
- `USER_ROLES_SETUP_GUIDE.md` - Detailed guide
- `config/database.py` - Database initialization

---

## 🆘 Troubleshooting

### "role='lecturer' not valid"
Run: `python migrate_lecturer_role.py`

### "course_lecturers table doesn't exist"
Run: `python migrate_lecturer_role.py`

### Cannot login as lecturer
1. Check email: `lecturer1@example.com`
2. Check password: `lecturer123`
3. Verify role: `SELECT role FROM users WHERE email='lecturer1@example.com'`

---

## 📞 Support

For detailed documentation, see:
- `USER_ROLES_SETUP_GUIDE.md`
- `BATCH_FILES_GUIDE.md`
