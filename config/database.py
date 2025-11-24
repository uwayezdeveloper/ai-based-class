import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ai_lms'
}

def create_database():
    """Create database if it doesn't exist"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        conn.close()
        print(f"✓ Database '{DB_CONFIG['database']}' created/verified successfully")
        return True
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def get_db_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Create all required tables"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'hod', 'student') NOT NULL,
            department_id INT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_role (role),
            INDEX idx_department (department_id)
        )
    ''')
    
    # Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_name (name)
        )
    ''')
    
    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            code VARCHAR(50) NOT NULL,
            description TEXT,
            department_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            INDEX idx_department (department_id),
            INDEX idx_code (code)
        )
    ''')
    
    # Materials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            file_path VARCHAR(500) NOT NULL,
            course_id INT NOT NULL,
            department_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            INDEX idx_course (course_id),
            INDEX idx_department (department_id)
        )
    ''')
    
    # Quizzes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            duration INT NOT NULL COMMENT 'Duration in minutes',
            questions JSON NOT NULL,
            course_id INT NOT NULL,
            department_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            INDEX idx_course (course_id),
            INDEX idx_department (department_id)
        )
    ''')
    
    # Quiz submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            quiz_id INT NOT NULL,
            user_id INT NOT NULL,
            answers JSON NOT NULL,
            score DECIMAL(5,2) NOT NULL,
            course_id INT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            INDEX idx_quiz (quiz_id),
            INDEX idx_user (user_id),
            INDEX idx_course (course_id),
            UNIQUE KEY unique_submission (quiz_id, user_id)
        )
    ''')
    
    # Chat history table (for AI chatbot)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            department_id INT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user (user_id),
            INDEX idx_department (department_id)
        )
    ''')
    
    # PDF embeddings table (for AI chatbot RAG)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_embeddings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            material_id INT NOT NULL,
            course_id INT NOT NULL,
            department_id INT NOT NULL,
            chunk_text TEXT NOT NULL,
            chunk_index INT NOT NULL,
            embedding_vector TEXT NOT NULL COMMENT 'JSON serialized vector',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            INDEX idx_material (material_id),
            INDEX idx_course (course_id),
            INDEX idx_department (department_id)
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ All tables created successfully")
    return True

def insert_default_data():
    """Insert default admin, HOD, and student users"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT id FROM users WHERE email = 'admin@gmail.com'")
    if not cursor.fetchone():
        # Create default admin
        admin_password = generate_password_hash('admin@gmail.com')
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            ('Admin User', 'admin@gmail.com', admin_password, 'admin')
        )
        print("✓ Default admin user created (email: admin@gmail.com, password: admin@gmail.com)")
    
    # Create sample department if none exists
    cursor.execute("SELECT id FROM departments LIMIT 1")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO departments (name, description) VALUES (%s, %s)",
            ('Computer Science', 'Department of Computer Science and Engineering')
        )
        dept_id = cursor.lastrowid
        
        cursor.execute(
            "INSERT INTO departments (name, description) VALUES (%s, %s)",
            ('Mathematics', 'Department of Mathematics')
        )
        
        print("✓ Sample departments created")
        
        # Create default HOD for Computer Science
        cursor.execute("SELECT id FROM users WHERE email = 'hod@gmail.com'")
        if not cursor.fetchone():
            hod_password = generate_password_hash('hod@gmail.com')
            cursor.execute(
                "INSERT INTO users (name, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)",
                ('HOD User', 'hod@gmail.com', hod_password, 'hod', dept_id)
            )
            print("✓ Default HOD user created (email: hod@gmail.com, password: hod@gmail.com)")
        
        # Create default student
        cursor.execute("SELECT id FROM users WHERE email = 'student@gmail.com'")
        if not cursor.fetchone():
            student_password = generate_password_hash('student@gmail.com')
            cursor.execute(
                "INSERT INTO users (name, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)",
                ('Student User', 'student@gmail.com', student_password, 'student', dept_id)
            )
            print("✓ Default student user created (email: student@gmail.com, password: student@gmail.com)")
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

def init_database():
    """Initialize database with tables and default data"""
    print("\n" + "="*50)
    print("Initializing AI-Powered Learning Management System")
    print("="*50 + "\n")
    
    if not create_database():
        print("\n✗ Database initialization failed!")
        return False
    
    if not create_tables():
        print("\n✗ Table creation failed!")
        return False
    
    if not insert_default_data():
        print("\n✗ Default data insertion failed!")
        return False
    
    print("\n" + "="*50)
    print("Database initialized successfully!")
    print("="*50)
    print("\nDefault Login Credentials:")
    print("-" * 50)
    print("Admin   : admin@gmail.com / admin@gmail.com")
    print("HOD     : hod@gmail.com / hod@gmail.com")
    print("Student : student@gmail.com / student@gmail.com")
    print("-" * 50)
    print("\nSystem ready! Access at: http://localhost:5000\n")
    
    return True

if __name__ == '__main__':
    init_database()
