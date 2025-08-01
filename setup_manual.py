"""
Manual setup script for the Employee-Employer System
Run this with: python setup_manual.py
"""

import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee, LeaveRequest
from datetime import date, timedelta
import random

def create_users():
    print("Creating users...")
    
    # Create superuser/admin
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@company.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        Employee.objects.create(
            user=admin_user,
            position='CEO',
            department='Management',
            is_employer=True,
            date_of_hire=date(2020, 1, 1)
        )
        print("✓ Created admin user (username: admin, password: admin123)")

    # Create employer
    if not User.objects.filter(username='employer').exists():
        employer_user = User.objects.create_user(
            username='employer',
            email='employer@company.com',
            password='employer123',
            first_name='John',
            last_name='Manager'
        )
        
        Employee.objects.create(
            user=employer_user,
            position='HR Manager',
            department='Human Resources',
            is_employer=True,
            date_of_hire=date(2021, 3, 15)
        )
        print("✓ Created employer user (username: employer, password: employer123)")

    # Sample employees
    employees_data = [
        {
            'username': 'alice_smith',
            'email': 'alice.smith@company.com',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'position': 'Software Developer',
            'department': 'Information Technology',
            'hire_date': date(2022, 6, 1)
        },
        {
            'username': 'bob_johnson',
            'email': 'bob.johnson@company.com',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'position': 'Marketing Specialist',
            'department': 'Marketing',
            'hire_date': date(2022, 8, 15)
        },
        {
            'username': 'carol_williams',
            'email': 'carol.williams@company.com',
            'first_name': 'Carol',
            'last_name': 'Williams',
            'position': 'Financial Analyst',
            'department': 'Finance',
            'hire_date': date(2023, 1, 10)
        }
    ]

    # Create employees
    for emp_data in employees_data:
        if not User.objects.filter(username=emp_data['username']).exists():
            user = User.objects.create_user(
                username=emp_data['username'],
                email=emp_data['email'],
                password='password123',
                first_name=emp_data['first_name'],
                last_name=emp_data['last_name']
            )
            
            Employee.objects.create(
                user=user,
                position=emp_data['position'],
                department=emp_data['department'],
                is_employer=False,
                date_of_hire=emp_data['hire_date']
            )
            print(f"✓ Created employee: {emp_data['first_name']} {emp_data['last_name']}")

    # Create sample leave requests
    employees = Employee.objects.filter(is_employer=False)
    reasons = [
        'Annual vacation',
        'Family emergency',
        'Medical appointment',
        'Personal matters',
        'Wedding attendance'
    ]

    for employee in employees:
        # Create 1-3 leave requests per employee
        num_requests = random.randint(1, 3)
        
        for _ in range(num_requests):
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            duration = random.randint(1, 5)
            end_date = start_date + timedelta(days=duration - 1)
            
            LeaveRequest.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,
                reason=random.choice(reasons),
                status=random.choice(['Pending', 'Approved', 'Rejected'])
            )

    print("✓ Created sample leave requests")

if __name__ == '__main__':
    print("=== Employee-Employer System Setup ===")
    create_users()
    print("\n✅ Setup Complete!")
    print("\nLogin Credentials:")
    print("Admin: admin / admin123")
    print("Employer: employer / employer123")
    print("Employee: alice_smith / password123")
    print("\nTo start the server: python manage.py runserver")
    print("Then go to: http://127.0.0.1:8000/")
