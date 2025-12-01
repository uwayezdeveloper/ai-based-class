"""
Migration script to add Lecturer role and course assignments
"""
import mysql.connector
from config.database import get_db_connection

def add_lecturer_role():
    """Add lecturer role to the system"""
    conn = get_db_connection()
    if not conn:
        print("✗ Failed to connect to database")
        return False
    
    cursor = conn.cursor()
    
    try:
        print("Starting migration to add Lecturer role...")
        print()
        
        # Step 1: Modify users table to include 'lecturer' role
        print("[1/4] Updating users table to include 'lecturer' role...")
        cursor.execute("""
            ALTER TABLE users 
            MODIFY COLUMN role ENUM('admin', 'hod', 'lecturer', 'student') NOT NULL
        """)
        print("✓ Users table updated")
        print()
        
        # Step 2: Create course_assignments table
        print("[2/4] Creating course_assignments table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                lecturer_id INT NOT NULL,
                assigned_by INT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE KEY unique_assignment (course_id, lecturer_id),
                INDEX idx_course (course_id),
                INDEX idx_lecturer (lecturer_id),
                INDEX idx_assigned_by (assigned_by)
            )
        """)
        print("✓ course_assignments table created")
        print()
        
        # Step 3: Add lecturer_id to courses table for tracking
        print("[3/4] Adding lecturer_id to courses table...")
        try:
            cursor.execute("""
                ALTER TABLE courses 
                ADD COLUMN lecturer_id INT NULL AFTER department_id,
                ADD FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE SET NULL,
                ADD INDEX idx_lecturer (lecturer_id)
            """)
            print("✓ lecturer_id column added to courses")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠ lecturer_id column already exists")
            else:
                raise
        print()
        
        # Step 4: Add created_by to quizzes table
        print("[4/4] Adding created_by to quizzes table...")
        try:
            cursor.execute("""
                ALTER TABLE quizzes 
                ADD COLUMN created_by INT NULL AFTER department_id,
                ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
                ADD INDEX idx_created_by (created_by)
            """)
            print("✓ created_by column added to quizzes")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠ created_by column already exists")
            else:
                raise
        print()
        
        conn.commit()
        print("=" * 50)
        print("✓ Migration completed successfully!")
        print("=" * 50)
        print()
        print("New features enabled:")
        print("  ✓ Lecturer role added")
        print("  ✓ Course assignment system created")
        print("  ✓ Lecturers can be assigned to courses")
        print("  ✓ Quiz tracking by creator")
        print()
        
        return True
        
    except mysql.connector.Error as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_lecturer_role()
