"""
Migration script to add missing columns to quiz_submissions table
Run this once to update the database schema
"""
import mysql.connector
from config.database import DB_CONFIG

def migrate():
    print("Starting migration...")
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ai_lms' 
            AND TABLE_NAME = 'quiz_submissions'
            AND COLUMN_NAME IN ('auto_score', 'manual_score', 'manual_marks', 'marking_status', 'feedback')
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        print(f"Found existing columns: {existing_columns}")
        
        # Add missing columns one by one
        if 'auto_score' not in existing_columns:
            print("Adding auto_score column...")
            cursor.execute("""
                ALTER TABLE quiz_submissions 
                ADD COLUMN auto_score DECIMAL(5,2) DEFAULT 0 AFTER score
            """)
            print("✓ Added auto_score")
        
        if 'manual_score' not in existing_columns:
            print("Adding manual_score column...")
            cursor.execute("""
                ALTER TABLE quiz_submissions 
                ADD COLUMN manual_score DECIMAL(5,2) DEFAULT NULL AFTER auto_score
            """)
            print("✓ Added manual_score")
        
        if 'manual_marks' not in existing_columns:
            print("Adding manual_marks column...")
            cursor.execute("""
                ALTER TABLE quiz_submissions 
                ADD COLUMN manual_marks JSON DEFAULT NULL AFTER manual_score
            """)
            print("✓ Added manual_marks")
        
        if 'marking_status' not in existing_columns:
            print("Adding marking_status column...")
            cursor.execute("""
                ALTER TABLE quiz_submissions 
                ADD COLUMN marking_status ENUM('pending', 'completed', 'partial') DEFAULT 'completed' AFTER manual_marks
            """)
            print("✓ Added marking_status")
        
        if 'feedback' not in existing_columns:
            print("Adding feedback column...")
            cursor.execute("""
                ALTER TABLE quiz_submissions 
                ADD COLUMN feedback TEXT DEFAULT NULL AFTER marking_status
            """)
            print("✓ Added feedback")
        
        conn.commit()
        
        print("\n✓ Migration completed successfully!")
        print("\nUpdated quiz_submissions table structure:")
        cursor.execute("DESCRIBE quiz_submissions")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
    return True

if __name__ == "__main__":
    migrate()
