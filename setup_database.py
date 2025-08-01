#!/usr/bin/env python
"""
Standalone database setup script for Employer-Employee System
This script bypasses Django management commands to avoid Python 3.13 compatibility issues
"""

import os
import sys
import sqlite3
from datetime import date, datetime

def hash_password(password):
    """Create a simple password hash (for demo purposes only)"""
    import hashlib
    # Simple hash for demo - in production use proper Django password hashing
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """Create and set up the SQLite database"""
    
    # Database file path
    db_path = 'db.sqlite3'
    
    print("🔧 Setting up database...")
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("   ✓ Removed existing database")
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Django tables
    print("   ✓ Creating Django system tables...")
    
    # Django migrations table
    cursor.execute('''
        CREATE TABLE django_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied DATETIME NOT NULL
        )
    ''')
    
    # Django content types
    cursor.execute('''
        CREATE TABLE django_content_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL
        )
    ''')
    
    # Auth permissions
    cursor.execute('''
        CREATE TABLE auth_permission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            content_type_id INTEGER NOT NULL,
            codename VARCHAR(100) NOT NULL,
            FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
        )
    ''')
    
    # Auth groups
    cursor.execute('''
        CREATE TABLE auth_group (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(150) UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE auth_group_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES auth_group (id),
            FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
        )
    ''')
    
    # Django sessions
    cursor.execute('''
        CREATE TABLE django_session (
            session_key VARCHAR(40) PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date DATETIME NOT NULL
        )
    ''')
    
    # Auth users table
    cursor.execute('''
        CREATE TABLE auth_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password VARCHAR(128) NOT NULL,
            last_login DATETIME,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) UNIQUE NOT NULL,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined DATETIME NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE auth_user_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES auth_user (id),
            FOREIGN KEY (group_id) REFERENCES auth_group (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE auth_user_user_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES auth_user (id),
            FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
        )
    ''')
    
    print("   ✓ Creating Employee app tables...")
    
    # Employee table
    cursor.execute('''
        CREATE TABLE employee_employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position VARCHAR(100) NOT NULL,
            department VARCHAR(100) NOT NULL,
            date_of_hire DATE NOT NULL,
            is_employer BOOLEAN NOT NULL,
            user_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES auth_user (id)
        )
    ''')
    
    # Leave requests table
    cursor.execute('''
        CREATE TABLE employee_leaverequest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            reason TEXT NOT NULL,
            status VARCHAR(20) NOT NULL,
            created_at DATETIME NOT NULL,
            employee_id INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employee_employee (id)
        )
    ''')
    
    print("   ✓ Database tables created successfully!")
    
    return conn, cursor

def create_users(cursor):
    """Create sample users and employees"""
    print("👥 Creating users...")
    
    now = datetime.now().isoformat()
    
    # Create superuser/admin
    admin_password = hash_password('admin123')
    cursor.execute('''
        INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (admin_password, None, 1, 'admin', 'Admin', 'User', 'admin@company.com', 1, 1, now))
    
    admin_user_id = cursor.lastrowid
    
    # Create admin employee profile
    cursor.execute('''
        INSERT INTO employee_employee (position, department, date_of_hire, is_employer, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ('CEO', 'Management', '2020-01-01', 1, admin_user_id))
    
    print("   ✓ Created admin user (admin/admin123)")
    
    # Create employer
    employer_password = hash_password('employer123')
    cursor.execute('''
        INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (employer_password, None, 0, 'employer', 'John', 'Manager', 'employer@company.com', 0, 1, now))
    
    employer_user_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO employee_employee (position, department, date_of_hire, is_employer, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ('HR Manager', 'Human Resources', '2021-03-15', 1, employer_user_id))
    
    print("   ✓ Created employer user (employer/employer123)")
    
    # Sample employees
    employees = [
        ('alice_smith', 'Alice', 'Smith', 'alice.smith@company.com', 'Software Developer', 'Information Technology', '2022-06-01'),
        ('bob_johnson', 'Bob', 'Johnson', 'bob.johnson@company.com', 'Marketing Specialist', 'Marketing', '2022-08-15'),
        ('carol_williams', 'Carol', 'Williams', 'carol.williams@company.com', 'Financial Analyst', 'Finance', '2023-01-10'),
        ('david_brown', 'David', 'Brown', 'david.brown@company.com', 'Sales Representative', 'Sales', '2023-04-20'),
        ('emma_davis', 'Emma', 'Davis', 'emma.davis@company.com', 'Customer Service Rep', 'Customer Service', '2023-07-05')
    ]
    
    employee_password = hash_password('password123')
    
    for username, first_name, last_name, email, position, department, hire_date in employees:
        # Create user
        cursor.execute('''
            INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_password, None, 0, username, first_name, last_name, email, 0, 1, now))
        
        user_id = cursor.lastrowid
        
        # Create employee profile
        cursor.execute('''
            INSERT INTO employee_employee (position, department, date_of_hire, is_employer, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (position, department, hire_date, 0, user_id))
        
        print(f"   ✓ Created employee: {first_name} {last_name} ({username}/password123)")

def create_sample_leave_requests(cursor):
    """Create sample leave requests"""
    print("📅 Creating sample leave requests...")
    
    import random
    from datetime import timedelta
    
    reasons = [
        'Annual vacation',
        'Family emergency',
        'Medical appointment',
        'Personal matters',
        'Wedding attendance',
        'Sick leave',
        'Conference attendance',
        'Moving to new house'
    ]
    
    statuses = ['Pending', 'Approved', 'Rejected']
    
    # Get employee IDs (exclude employers)
    cursor.execute('SELECT id FROM employee_employee WHERE is_employer = 0')
    employee_ids = [row[0] for row in cursor.fetchall()]
    
    for employee_id in employee_ids:
        # Create 2-3 leave requests per employee
        num_requests = random.randint(2, 3)
        
        for _ in range(num_requests):
            # Random dates
            days_offset = random.randint(-180, 90)
            start_date = date.today() + timedelta(days=days_offset)
            duration = random.randint(1, 7)
            end_date = start_date + timedelta(days=duration - 1)
            
            cursor.execute('''
                INSERT INTO employee_leaverequest (start_date, end_date, reason, status, created_at, employee_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                start_date.isoformat(),
                end_date.isoformat(),
                random.choice(reasons),
                random.choice(statuses),
                datetime.now().isoformat(),
                employee_id
            ))
    
    print(f"   ✓ Created sample leave requests")

def main():
    print("🚀 Employer-Employee System Database Setup")
    print("=" * 50)
    
    try:
        # Setup database
        conn, cursor = setup_database()
        
        # Create users
        create_users(cursor)
        
        # Create sample data
        create_sample_leave_requests(cursor)
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\n✅ Database setup completed successfully!")
        print("\n🔑 Login Credentials:")
        print("   Admin/Superuser: admin / admin123")
        print("   HR Manager: employer / employer123")
        print("   Sample Employee: alice_smith / password123")
        print("\n🌐 Next steps:")
        print("   1. Run: python manage.py runserver")
        print("   2. Open: http://127.0.0.1:8000/")
        print("   3. Login with any of the above credentials")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
