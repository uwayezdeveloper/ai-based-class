"""
AI-Powered Learning Management System
Installation Verification Script
"""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n✓ Checking required packages...")
    required_packages = [
        'flask',
        'mysql.connector',
        'werkzeug',
        'PyPDF2',
        'sentence_transformers',
        'numpy',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} not found")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_mysql_connection():
    """Check MySQL connection"""
    print("\n✓ Checking MySQL connection...")
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        conn.close()
        print("  ✓ MySQL connection successful")
        return True
    except Exception as e:
        print(f"  ✗ MySQL connection failed: {e}")
        print("  ⚠ Make sure XAMPP MySQL is running")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n✓ Checking directories...")
    directories = [
        'uploads',
        'uploads/pdfs',
        'templates',
        'config',
        'services'
    ]
    
    all_exist = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ not found")
            all_exist = False
    
    return all_exist

def check_required_files():
    """Check if required files exist"""
    print("\n✓ Checking required files...")
    files = [
        'app.py',
        'requirements.txt',
        'config/database.py',
        'services/ai_chatbot.py',
        'services/pdf_processor.py',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} not found")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("AI-Powered Learning Management System")
    print("Installation Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Check Python version
    results.append(("Python Version", check_python_version()))
    
    # Check packages
    packages_ok, missing = check_required_packages()
    results.append(("Required Packages", packages_ok))
    
    # Check MySQL
    results.append(("MySQL Connection", check_mysql_connection()))
    
    # Check directories
    results.append(("Directories", check_directories()))
    
    # Check files
    results.append(("Required Files", check_required_files()))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! System is ready to run.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open browser: http://localhost:5000")
        print("3. Login with default credentials (see README.md)")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        if not packages_ok:
            print("\nTo install missing packages, run:")
            print("  pip install -r requirements.txt")
        print("\nFor detailed help, see README.md or QUICKSTART.md")
    
    print()

if __name__ == '__main__':
    main()
