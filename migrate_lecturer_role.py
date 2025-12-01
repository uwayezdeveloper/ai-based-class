"""
Migration Script: Add Lecturer Role and Course Assignment System
Run this script to add lecturer functionality to the AI-LMS system
"""

import mysql.connector
from werkzeug.security import generate_password_hash
from config.database import get_db_connection

def migrate_lecturer_system():
    """Add lecturer role and course assignment tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("=" * 60)
        print("AI-LMS: Adding Lecturer Role System")
        print("=" * 60)
        print()
        
        # Step 1: Update users table role enum
        print("[1/8] Updating users table to include 'lecturer' role...")
        try:
            cursor.execute("""
                ALTER TABLE users 
                MODIFY COLUMN role ENUM('admin', 'hod', 'lecturer', 'student') 
                NOT NULL DEFAULT 'student'
            """)
            conn.commit()
            print("✓ Users table updated")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e) or "check that column" in str(e):
                print("✓ Users table already has lecturer role")
            else:
                raise
        print()
        
        # Step 2: Create course_lecturers table
        print("[2/8] Creating course_lecturers table...")
        cursor.execute("""
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
        print("✓ course_lecturers table created")
        print()
        
        # Step 3: Add default lecturer accounts
        print("[3/8] Adding default lecturer accounts...")
        lecturer_password = generate_password_hash('lecturer123')
        
        lecturers = [
            ('Dr. John Smith', 'lecturer1@example.com', 1),
            ('Prof. Sarah Johnson', 'lecturer2@example.com', 2),
            ('Dr. Michael Chen', 'lecturer3@example.com', 3)
        ]
        
        for name, email, dept_id in lecturers:
            try:
                cursor.execute("""
                    INSERT INTO users (name, email, password, role, department_id) 
                    VALUES (%s, %s, %s, 'lecturer', %s)
                    ON DUPLICATE KEY UPDATE role='lecturer', department_id=%s
                """, (name, email, lecturer_password, dept_id, dept_id))
                print(f"✓ Added lecturer: {name} ({email})")
            except Exception as e:
                print(f"  Note: {email} may already exist")
        
        conn.commit()
        print()
        
        # Step 4: Update admin role
        print("[4/8] Ensuring admin role is set correctly...")
        cursor.execute("""
            UPDATE users SET role = 'admin' 
            WHERE email = 'admin@example.com'
        """)
        conn.commit()
        print("✓ Admin role verified")
        print()
        
        # Step 5: Update HOD roles
        print("[5/8] Ensuring HOD roles are set correctly...")
        cursor.execute("""
            UPDATE users SET role = 'hod' 
            WHERE email LIKE 'hod%@example.com'
        """)
        conn.commit()
        print(f"✓ Updated {cursor.rowcount} HOD accounts")
        print()
        
        # Step 6: Auto-assign courses to lecturers in same department
        print("[6/8] Auto-assigning courses to lecturers...")
        cursor.execute("""
            INSERT INTO course_lecturers (course_id, lecturer_id, assigned_by)
            SELECT c.id, u.id, 
                   (SELECT id FROM users WHERE role='hod' AND department_id = c.department_id LIMIT 1)
            FROM courses c
            CROSS JOIN users u
            WHERE u.role = 'lecturer' 
            AND u.department_id = c.department_id
            AND NOT EXISTS (
                SELECT 1 FROM course_lecturers cl 
                WHERE cl.course_id = c.id AND cl.lecturer_id = u.id
            )
        """)
        conn.commit()
        print(f"✓ Created {cursor.rowcount} course assignments")
        print()
        
        # Step 7: Display role summary
        print("[7/8] User roles summary:")
        cursor.execute("""
            SELECT role, COUNT(*) as count 
            FROM users 
            GROUP BY role 
            ORDER BY FIELD(role, 'admin', 'hod', 'lecturer', 'student')
        """)
        roles = cursor.fetchall()
        for role, count in roles:
            print(f"  {role.upper()}: {count} user(s)")
        print()
        
        # Step 8: Display course assignments
        print("[8/8] Course assignments summary:")
        cursor.execute("""
            SELECT COUNT(*) as total FROM course_lecturers
        """)
        total = cursor.fetchone()[0]
        print(f"  Total assignments: {total}")
        
        cursor.execute("""
            SELECT u.name, u.email, COUNT(cl.id) as course_count
            FROM users u
            LEFT JOIN course_lecturers cl ON u.id = cl.lecturer_id
            WHERE u.role = 'lecturer'
            GROUP BY u.id
            ORDER BY u.name
        """)
        lecturers = cursor.fetchall()
        for name, email, count in lecturers:
            print(f"  {name} ({email}): {count} course(s)")
        print()
        
        cursor.close()
        conn.close()
        
        print("=" * 60)
        print("✓ Migration completed successfully!")
        print("=" * 60)
        print()
        print("DEFAULT CREDENTIALS:")
        print()
        print("ADMIN:")
        print("  Email: admin@example.com")
        print("  Password: admin123")
        print()
        print("HOD:")
        print("  Email: hod@example.com")
        print("  Password: hod123")
        print()
        print("LECTURERS:")
        print("  Email: lecturer1@example.com")
        print("  Password: lecturer123")
        print()
        print("  Email: lecturer2@example.com")
        print("  Password: lecturer123")
        print()
        print("  Email: lecturer3@example.com")
        print("  Password: lecturer123")
        print()
        print("STUDENTS:")
        print("  Register through the registration page")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\nStarting lecturer role migration...\n")
    success = migrate_lecturer_system()
    
    if success:
        print("\n✓ You can now run the application with: python app.py")
    else:
        print("\n✗ Migration failed. Please check the errors above.")
    
    input("\nPress Enter to exit...")
