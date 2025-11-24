from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime, timedelta
import json
from functools import wraps
from config.database import init_database, get_db_connection
from services.ai_chatbot import AIChatbot
from services.pdf_processor import PDFProcessor

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs'), exist_ok=True)

# Initialize AI Chatbot
chatbot = AIChatbot()
pdf_processor = PDFProcessor()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            session['name'] = user['name']
            session['department_id'] = user['department_id']
            session.permanent = True
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        department_id = request.form.get('department_id')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('Email already registered', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        
        # Create new student account
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (name, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)',
            (name, email, hashed_password, 'student', department_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    # Get departments for registration form
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name FROM departments')
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('register.html', departments=departments)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'hod':
        return redirect(url_for('hod_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))

# Admin Routes
@app.route('/admin/dashboard')
@role_required(['admin'])
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as count FROM departments')
    dept_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE role = "hod"')
    hod_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE role = "student"')
    student_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM courses')
    course_count = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    
    return render_template('admin/dashboard.html', 
                         dept_count=dept_count, 
                         hod_count=hod_count,
                         student_count=student_count,
                         course_count=course_count)

@app.route('/admin/departments', methods=['GET', 'POST'])
@role_required(['admin'])
def admin_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        cursor.execute('INSERT INTO departments (name, description) VALUES (%s, %s)', 
                      (name, description))
        conn.commit()
        flash('Department created successfully', 'success')
    
    cursor.execute('SELECT * FROM departments ORDER BY created_at DESC')
    departments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/departments.html', departments=departments)

@app.route('/admin/hods', methods=['GET', 'POST'])
@role_required(['admin'])
def admin_hods():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password', 'hod@gmail.com')  # Default password
        department_id = request.form.get('department_id')
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('Email already exists', 'error')
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute(
                'INSERT INTO users (name, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)',
                (name, email, hashed_password, 'hod', department_id)
            )
            conn.commit()
            flash('HOD added successfully', 'success')
    
    cursor.execute('''
        SELECT u.*, d.name as department_name 
        FROM users u 
        LEFT JOIN departments d ON u.department_id = d.id 
        WHERE u.role = "hod"
        ORDER BY u.created_at DESC
    ''')
    hods = cursor.fetchall()
    
    cursor.execute('SELECT id, name FROM departments')
    departments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/hods.html', hods=hods, departments=departments)

# HOD Routes
@app.route('/hod/dashboard')
@role_required(['hod'])
def hod_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as count FROM courses WHERE department_id = %s', (dept_id,))
    course_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM materials WHERE department_id = %s', (dept_id,))
    material_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM quizzes WHERE department_id = %s', (dept_id,))
    quiz_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT name FROM departments WHERE id = %s', (dept_id,))
    department = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('hod/dashboard.html',
                         course_count=course_count,
                         material_count=material_count,
                         quiz_count=quiz_count,
                         department=department)

@app.route('/hod/courses', methods=['GET', 'POST'])
@role_required(['hod'])
def hod_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        description = request.form.get('description')
        
        cursor.execute(
            'INSERT INTO courses (name, code, description, department_id) VALUES (%s, %s, %s, %s)',
            (name, code, description, dept_id)
        )
        conn.commit()
        flash('Course added successfully', 'success')
    
    cursor.execute('SELECT * FROM courses WHERE department_id = %s ORDER BY created_at DESC', (dept_id,))
    courses = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('hod/courses.html', courses=courses)

@app.route('/hod/materials/<int:course_id>', methods=['GET', 'POST'])
@role_required(['hod'])
def hod_materials(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Verify course belongs to HOD's department
    cursor.execute('SELECT * FROM courses WHERE id = %s AND department_id = %s', (course_id, dept_id))
    course = cursor.fetchone()
    
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('hod_courses'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('file')
        
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs', filename)
            file.save(filepath)
            
            # Process PDF for AI chatbot
            pdf_processor.process_pdf(filepath, course_id)
            
            cursor.execute(
                'INSERT INTO materials (title, description, file_path, course_id, department_id) VALUES (%s, %s, %s, %s, %s)',
                (title, description, filename, course_id, dept_id)
            )
            conn.commit()
            flash('Material uploaded successfully', 'success')
        else:
            flash('Please upload a PDF file', 'error')
    
    cursor.execute('SELECT * FROM materials WHERE course_id = %s ORDER BY created_at DESC', (course_id,))
    materials = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('hod/materials.html', course=course, materials=materials)

@app.route('/hod/quizzes/<int:course_id>', methods=['GET', 'POST'])
@role_required(['hod'])
def hod_quizzes(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Verify course belongs to HOD's department
    cursor.execute('SELECT * FROM courses WHERE id = %s AND department_id = %s', (course_id, dept_id))
    course = cursor.fetchone()
    
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('hod_courses'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        duration = request.form.get('duration')
        questions = request.form.get('questions')  # JSON string
        
        cursor.execute(
            'INSERT INTO quizzes (title, description, duration, questions, course_id, department_id) VALUES (%s, %s, %s, %s, %s, %s)',
            (title, description, duration, questions, course_id, dept_id)
        )
        conn.commit()
        flash('Quiz created successfully', 'success')
        return redirect(url_for('hod_quizzes', course_id=course_id))
    
    cursor.execute('SELECT * FROM quizzes WHERE course_id = %s ORDER BY created_at DESC', (course_id,))
    quizzes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('hod/quizzes.html', course=course, quizzes=quizzes)

@app.route('/hod/quiz/create/<int:course_id>')
@role_required(['hod'])
def hod_create_quiz(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    cursor.execute('SELECT * FROM courses WHERE id = %s AND department_id = %s', (course_id, dept_id))
    course = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('hod_courses'))
    
    return render_template('hod/create_quiz.html', course=course)

@app.route('/hod/quiz/<int:quiz_id>/submissions')
@role_required(['hod'])
def hod_quiz_submissions(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Get quiz and verify department
    cursor.execute('SELECT q.*, c.name as course_name FROM quizzes q JOIN courses c ON q.course_id = c.id WHERE q.id = %s AND q.department_id = %s', (quiz_id, dept_id))
    quiz = cursor.fetchone()
    
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('hod_dashboard'))
    
    # Get course
    cursor.execute('SELECT * FROM courses WHERE id = %s', (quiz['course_id'],))
    course = cursor.fetchone()
    
    # Get all submissions with student info
    cursor.execute('''
        SELECT qs.*, u.name as student_name, u.email as student_email
        FROM quiz_submissions qs
        JOIN users u ON qs.user_id = u.id
        WHERE qs.quiz_id = %s
        ORDER BY qs.submitted_at DESC
    ''', (quiz_id,))
    submissions = cursor.fetchall()
    
    # Calculate total points
    questions = json.loads(quiz['questions'])
    total_points = sum(q.get('points', 10) for q in questions)
    
    # Calculate average score
    avg_score = 0
    if submissions:
        total_score = sum(s['score'] for s in submissions)
        avg_score = (total_score / len(submissions) / total_points * 100) if total_points > 0 else 0
    
    cursor.close()
    conn.close()
    
    return render_template('hod/quiz_submissions.html', 
                         quiz=quiz, 
                         course=course, 
                         submissions=submissions,
                         total_points=total_points,
                         avg_score=avg_score)

@app.route('/hod/submission/<int:submission_id>/mark', methods=['GET', 'POST'])
@role_required(['hod'])
def hod_mark_submission(submission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Get submission with student info
    cursor.execute('''
        SELECT qs.*, u.name as student_name, u.email as student_email, q.department_id
        FROM quiz_submissions qs
        JOIN users u ON qs.user_id = u.id
        JOIN quizzes q ON qs.quiz_id = q.id
        WHERE qs.id = %s AND q.department_id = %s
    ''', (submission_id, dept_id))
    submission = cursor.fetchone()
    
    if not submission:
        flash('Submission not found', 'error')
        return redirect(url_for('hod_dashboard'))
    
    # Get quiz
    cursor.execute('SELECT * FROM quizzes WHERE id = %s', (submission['quiz_id'],))
    quiz = cursor.fetchone()
    
    questions = json.loads(quiz['questions'])
    answers = json.loads(submission['answers'])
    
    if request.method == 'POST':
        data = request.json
        manual_score = 0
        manual_marks = {}
        
        # Calculate manual score from open-ended questions
        for i, question in enumerate(questions):
            if question.get('type') == 'open_ended':
                points_key = f'question_{i}_points'
                feedback_key = f'question_{i}_feedback'
                
                points = float(data.get(points_key, 0))
                feedback = data.get(feedback_key, '')
                
                manual_score += points
                manual_marks[str(i)] = {
                    'points': points,
                    'feedback': feedback
                }
        
        # Update submission
        total_score = (submission['auto_score'] or 0) + manual_score
        general_feedback = data.get('general_feedback', '')
        
        cursor.execute('''
            UPDATE quiz_submissions 
            SET manual_score = %s, 
                score = %s, 
                marking_status = 'completed',
                marked_by = %s,
                marked_at = NOW(),
                feedback = %s
            WHERE id = %s
        ''', (manual_score, total_score, session['user_id'], general_feedback, submission_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True})
    
    # Calculate total points
    total_points = sum(q.get('points', 10) for q in questions)
    
    # Get manual marks if already marked
    manual_marks = {}
    if submission.get('feedback'):
        # Parse feedback for manual marks (you can enhance this)
        pass
    
    cursor.close()
    conn.close()
    
    return render_template('hod/mark_submission.html',
                         submission=submission,
                         quiz=quiz,
                         questions=questions,
                         answers=answers,
                         total_points=total_points,
                         manual_marks=manual_marks,
                         enumerate=enumerate)

@app.route('/hod/quiz/<int:quiz_id>/report')
@role_required(['hod'])
def hod_generate_report(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    # Get quiz
    cursor.execute('''
        SELECT q.*, c.name as course_name, d.name as department_name 
        FROM quizzes q 
        JOIN courses c ON q.course_id = c.id
        JOIN departments d ON q.department_id = d.id
        WHERE q.id = %s AND q.department_id = %s
    ''', (quiz_id, dept_id))
    quiz = cursor.fetchone()
    
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('hod_dashboard'))
    
    # Get all submissions
    cursor.execute('''
        SELECT qs.*, u.name as student_name, u.email as student_email
        FROM quiz_submissions qs
        JOIN users u ON qs.user_id = u.id
        WHERE qs.quiz_id = %s
        ORDER BY qs.score DESC, u.name
    ''', (quiz_id,))
    submissions = cursor.fetchall()
    
    # Calculate statistics
    questions = json.loads(quiz['questions'])
    total_points = sum(q.get('points', 10) for q in questions)
    
    stats = {
        'total_submissions': len(submissions),
        'completed': sum(1 for s in submissions if s['marking_status'] == 'completed'),
        'pending': sum(1 for s in submissions if s['marking_status'] == 'pending'),
        'avg_score': 0,
        'highest_score': 0,
        'lowest_score': 0
    }
    
    if submissions:
        scores = [s['score'] for s in submissions]
        stats['avg_score'] = sum(scores) / len(scores)
        stats['highest_score'] = max(scores)
        stats['lowest_score'] = min(scores)
    
    cursor.close()
    conn.close()
    
    from datetime import datetime
    return render_template('hod/quiz_report.html',
                         quiz=quiz,
                         submissions=submissions,
                         total_points=total_points,
                         stats=stats,
                         now=datetime.now)

# Student Routes
@app.route('/student/dashboard')
@role_required(['student'])
def student_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    dept_id = session.get('department_id')
    
    if dept_id:
        cursor.execute('SELECT name FROM departments WHERE id = %s', (dept_id,))
        department = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) as count FROM courses WHERE department_id = %s', (dept_id,))
        course_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM materials WHERE department_id = %s', (dept_id,))
        material_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM quiz_submissions WHERE user_id = %s', (session['user_id'],))
        quiz_count = cursor.fetchone()['count']
    else:
        department = None
        course_count = 0
        material_count = 0
        quiz_count = 0
    
    cursor.close()
    conn.close()
    
    return render_template('student/dashboard.html',
                         department=department,
                         course_count=course_count,
                         material_count=material_count,
                         quiz_count=quiz_count)

@app.route('/student/departments')
@role_required(['student'])
def student_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM departments ORDER BY name')
    departments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('student/departments.html', departments=departments)

@app.route('/student/select-department/<int:dept_id>')
@role_required(['student'])
def student_select_department(dept_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Update student's department
    cursor.execute('UPDATE users SET department_id = %s WHERE id = %s', (dept_id, session['user_id']))
    conn.commit()
    
    cursor.execute('SELECT name FROM departments WHERE id = %s', (dept_id,))
    dept = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    session['department_id'] = dept_id
    flash(f'Department changed to {dept["name"]}', 'success')
    return redirect(url_for('student_courses'))

@app.route('/student/courses')
@role_required(['student'])
def student_courses():
    dept_id = session.get('department_id')
    
    if not dept_id:
        flash('Please select a department first', 'warning')
        return redirect(url_for('student_departments'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM courses WHERE department_id = %s ORDER BY name', (dept_id,))
    courses = cursor.fetchall()
    
    cursor.execute('SELECT name FROM departments WHERE id = %s', (dept_id,))
    department = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('student/courses.html', courses=courses, department=department)

@app.route('/student/materials/<int:course_id>')
@role_required(['student'])
def student_materials(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('student_courses'))
    
    cursor.execute('SELECT * FROM materials WHERE course_id = %s ORDER BY created_at DESC', (course_id,))
    materials = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('student/materials.html', course=course, materials=materials)

@app.route('/student/view-pdf/<int:material_id>')
@role_required(['student'])
def student_view_pdf(material_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM materials WHERE id = %s', (material_id,))
    material = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not material:
        flash('Material not found', 'error')
        return redirect(url_for('student_courses'))
    
    return render_template('student/view_pdf.html', material=material)

@app.route('/uploads/pdfs/<filename>')
@login_required
def serve_pdf(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs'), filename)

@app.route('/student/quizzes/<int:course_id>')
@role_required(['student'])
def student_quizzes(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
    course = cursor.fetchone()
    
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('student_courses'))
    
    cursor.execute('SELECT * FROM quizzes WHERE course_id = %s ORDER BY created_at DESC', (course_id,))
    quizzes = cursor.fetchall()
    
    # Get student's submissions
    cursor.execute('SELECT quiz_id, score, submitted_at FROM quiz_submissions WHERE user_id = %s', (session['user_id'],))
    submissions = {sub['quiz_id']: sub for sub in cursor.fetchall()}
    
    cursor.close()
    conn.close()
    
    return render_template('student/quizzes.html', course=course, quizzes=quizzes, submissions=submissions)

@app.route('/student/take-quiz/<int:quiz_id>')
@role_required(['student'])
def student_take_quiz(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if already submitted
    cursor.execute('SELECT id FROM quiz_submissions WHERE quiz_id = %s AND user_id = %s', 
                  (quiz_id, session['user_id']))
    if cursor.fetchone():
        flash('You have already submitted this quiz', 'warning')
        cursor.close()
        conn.close()
        return redirect(url_for('student_dashboard'))
    
    cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
    quiz = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('student_courses'))
    
    # Parse questions
    quiz['questions'] = json.loads(quiz['questions'])
    
    return render_template('student/take_quiz.html', quiz=quiz)

@app.route('/student/submit-quiz/<int:quiz_id>', methods=['POST'])
@role_required(['student'])
def student_submit_quiz(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get quiz
    cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
    quiz = cursor.fetchone()
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Calculate score for auto-markable questions
    questions = json.loads(quiz['questions'])
    answers = request.json.get('answers', {})
    
    auto_correct = 0
    auto_total_points = 0
    manual_total_points = 0
    total_points = 0
    has_manual_questions = False
    
    for i, question in enumerate(questions):
        question_type = question.get('type', 'multiple_choice')
        points = question.get('points', 10)
        total_points += points
        
        if question_type == 'open_ended':
            # Manual marking required
            has_manual_questions = True
            manual_total_points += points
        else:
            # Auto-markable question
            auto_total_points += points
            if str(i) in answers:
                # Check if answer is correct
                student_answer = answers[str(i)]
                correct_answer = question.get('correct')
                
                # Handle multiple correct answers (array) or single answer (int)
                if isinstance(correct_answer, list):
                    # Multiple correct answers - student answer should also be a list
                    if isinstance(student_answer, list):
                        # Check if student selected exactly the right answers
                        if sorted(student_answer) == sorted(correct_answer):
                            auto_correct += points
                    elif len(correct_answer) == 1 and student_answer == correct_answer[0]:
                        # Single checkbox selected matching single correct answer
                        auto_correct += points
                elif isinstance(student_answer, int) and student_answer == correct_answer:
                    # Single answer question
                    auto_correct += points
                elif isinstance(student_answer, list) and len(student_answer) == 1 and student_answer[0] == correct_answer:
                    # Student submitted as list but answer is single
                    auto_correct += points
    
    # Calculate auto_score
    auto_score = auto_correct
    
    # Determine marking status
    if has_manual_questions:
        marking_status = 'pending'  # Requires manual marking
    else:
        marking_status = 'completed'  # All auto-marked
    
    # Total score (only auto for now, manual will be added by HOD)
    total_score = auto_score
    
    # Save submission
    cursor.execute('''
        INSERT INTO quiz_submissions 
        (quiz_id, user_id, answers, score, auto_score, manual_score, marking_status, course_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (quiz_id, session['user_id'], json.dumps(answers), total_score, auto_score, 
          None, marking_status, quiz['course_id']))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    # Calculate percentage
    score_percentage = (total_score / total_points * 100) if total_points > 0 else 0
    
    return jsonify({
        'score': score_percentage,
        'points': total_score,
        'total_points': total_points,
        'auto_points': auto_score,
        'auto_total_points': auto_total_points,
        'manual_total_points': manual_total_points,
        'requires_manual_marking': has_manual_questions,
        'marking_status': marking_status
    })

# AI Chatbot Routes
@app.route('/student/chatbot')
@role_required(['student'])
def student_chatbot():
    return render_template('student/chatbot.html')

@app.route('/api/chatbot/message', methods=['POST'])
@role_required(['student'])
def chatbot_message():
    data = request.json
    message = data.get('message', '')
    department_id = session.get('department_id')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Get AI response
    response = chatbot.get_response(message, department_id)
    
    return jsonify({'response': response})

# API Routes for AJAX
@app.route('/api/departments')
@login_required
def api_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, description FROM departments')
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(departments)

@app.route('/api/courses/<int:department_id>')
@login_required
def api_courses(department_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, code, description FROM courses WHERE department_id = %s', (department_id,))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(courses)

if __name__ == '__main__':
    # Initialize database on first run
    init_database()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
