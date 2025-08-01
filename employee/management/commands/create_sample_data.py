from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employee.models import Employee, LeaveRequest
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample data for the Employee-Employer System'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create superuser/employer
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
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))

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
            self.stdout.write(self.style.SUCCESS('Created employer user (username: employer, password: employer123)'))

        # Sample employees data
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
            },
            {
                'username': 'david_brown',
                'email': 'david.brown@company.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'position': 'Sales Representative',
                'department': 'Sales',
                'hire_date': date(2023, 4, 20)
            },
            {
                'username': 'emma_davis',
                'email': 'emma.davis@company.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'position': 'Customer Service Rep',
                'department': 'Customer Service',
                'hire_date': date(2023, 7, 5)
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
                self.stdout.write(f'Created employee: {emp_data["first_name"]} {emp_data["last_name"]}')

        # Create sample leave requests
        employees = Employee.objects.filter(is_employer=False)
        statuses = ['Pending', 'Approved', 'Rejected']
        reasons = [
            'Annual vacation',
            'Family emergency',
            'Medical appointment',
            'Personal matters',
            'Wedding attendance',
            'Sick leave',
            'Maternity leave',
            'Conference attendance',
            'Moving to new house',
            'Mental health day'
        ]

        for employee in employees:
            # Create 2-5 leave requests per employee
            num_requests = random.randint(2, 5)
            
            for _ in range(num_requests):
                # Random start date within the past 6 months to next 3 months
                start_date = date.today() + timedelta(days=random.randint(-180, 90))
                duration = random.randint(1, 10)  # 1-10 days
                end_date = start_date + timedelta(days=duration - 1)
                
                LeaveRequest.objects.create(
                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,
                    reason=random.choice(reasons),
                    status=random.choice(statuses)
                )

        self.stdout.write(self.style.SUCCESS('Created sample leave requests'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully! ==='))
        self.stdout.write(self.style.SUCCESS('\nLogin Credentials:'))
        self.stdout.write(self.style.SUCCESS('Admin/Employer: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('HR Manager: employer / employer123'))
        self.stdout.write(self.style.SUCCESS('Employees: alice_smith, bob_johnson, carol_williams, david_brown, emma_davis / password123'))
        self.stdout.write(self.style.SUCCESS('\nYou can now run the server and test the application!'))
