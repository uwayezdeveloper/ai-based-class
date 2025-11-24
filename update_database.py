"""
Database migration script to update quiz system for different question types
"""
import mysql.connector
from config.database import get_db_connection

def update_database():
    """Update database schema for enhanced quiz functionality"""
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return False
    
    cursor = conn.cursor()
    
    try:
        print("🔄 Updating database schema...")
        
        # Modify quiz_submissions table to support auto and manual marking
        print("  - Updating quiz_submissions table...")
        
        # Add new columns for enhanced quiz functionality
        queries = [
            # Add auto_score for automatically marked questions
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS auto_score DECIMAL(5,2) DEFAULT 0 
            COMMENT 'Score from auto-marked questions'
            """,
            
            # Add manual_score for manually marked questions
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS manual_score DECIMAL(5,2) DEFAULT NULL 
            COMMENT 'Score from manually marked questions'
            """,
            
            # Add total_score (calculated from auto + manual)
            """
            ALTER TABLE quiz_submissions 
            MODIFY COLUMN score DECIMAL(5,2) DEFAULT 0 
            COMMENT 'Total score (auto + manual)'
            """,
            
            # Add marking status
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS marking_status ENUM('pending', 'partially_marked', 'completed') 
            DEFAULT 'pending' 
            COMMENT 'Status of manual marking'
            """,
            
            # Add marked_by to track who marked the submission
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS marked_by INT NULL 
            COMMENT 'User ID of HOD who marked manually'
            """,
            
            # Add marked_at timestamp
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS marked_at TIMESTAMP NULL 
            COMMENT 'When manual marking was completed'
            """,
            
            # Add feedback for manual marking
            """
            ALTER TABLE quiz_submissions 
            ADD COLUMN IF NOT EXISTS feedback TEXT NULL 
            COMMENT 'Feedback from HOD on manually marked questions'
            """
        ]
        
        for query in queries:
            try:
                cursor.execute(query)
                conn.commit()
            except mysql.connector.Error as e:
                # Ignore duplicate column errors
                if "Duplicate column" not in str(e):
                    print(f"    ⚠ Warning: {e}")
        
        print("  ✓ quiz_submissions table updated")
        
        print("\n✅ Database schema updated successfully!")
        print("\n📋 New Quiz Features:")
        print("  • Multiple question types (MCQ, Yes/No, True/False, Open-ended)")
        print("  • Auto-marking for objective questions")
        print("  • Manual marking for subjective questions")
        print("  • Detailed feedback system")
        print("  • Report generation")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error updating database: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Enhanced Quiz System")
    print("=" * 60)
    update_database()
