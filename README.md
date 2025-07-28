# Employer-Employee Management System

A comprehensive Django-based web application for managing employer-employee interactions, focusing on employee self-service and leave management with role-based access control.

## Features

### 🏢 **For Employers**
- **Comprehensive Dashboard**: View all employees, leave requests, and system statistics
- **Leave Management**: Approve or reject employee leave requests with one click
- **Employee Overview**: Monitor all employees with their departments, positions, and hire dates
- **Real-time Analytics**: Track pending, approved, and rejected leave requests
- **Search & Filter**: Easily find employees and filter leave requests by status

### 👥 **For Employees**
- **Personal Dashboard**: View profile summary, leave statistics, and recent activity
- **Leave Request System**: Submit detailed leave requests with date validation
- **Request Tracking**: Monitor the status of all submitted leave requests
- **Profile Management**: Update personal and work information
- **Intuitive Interface**: User-friendly design with quick action buttons

### 🔐 **Security & Access Control**
- **Role-Based Access**: Automatic role detection and appropriate dashboard routing
- **Secure Authentication**: Django's built-in authentication system
- **Permission Management**: Employers can only access authorized features
- **User Profile Integration**: Seamless integration with Django's User model

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Bootstrap 5**: Modern, clean interface with smooth animations
- **Interactive Elements**: Real-time form validation and dynamic content
- **Accessibility Ready**: Semantic HTML and ARIA labels for screen readers

## Quick Start

### Option 1: Automated Setup (Windows)
Run the setup script to automatically configure everything:
```bash
setup.bat
```

### Option 2: Manual Setup

1. **Clone the repository**:
```bash
git clone https://github.com/ChrisDevCode-Technologies/20django-employer-employee-delta.git
cd 20django-employer-employee-delta
```

2. **Create and activate virtual environment**:
```bash
# Windows
py -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create sample data** (optional but recommended):
```bash
python manage.py create_sample_data
```

6. **Start the development server**:
```bash
python manage.py runserver
```

7. **Access the application**:
   - Open your browser and go to `http://127.0.0.1:8000/`

## Default Login Credentials

After running the sample data creation command, you can use these accounts:

### Employers/Admins
- **Super Admin**: `admin` / `admin123`
- **HR Manager**: `employer` / `employer123`

### Sample Employees
- **Alice Smith**: `alice_smith` / `password123` (Software Developer, IT)
- **Bob Johnson**: `bob_johnson` / `password123` (Marketing Specialist, Marketing)
- **Carol Williams**: `carol_williams` / `password123` (Financial Analyst, Finance)
- **David Brown**: `david_brown` / `password123` (Sales Representative, Sales)
- **Emma Davis**: `emma_davis` / `password123` (Customer Service Rep, Customer Service)

## Project Structure

```
20django-employer-employee-delta/
├── core/                      # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── employee/                 # Main application
│   ├── models.py            # Employee and LeaveRequest models
│   ├── views.py             # Dashboard and authentication views
│   ├── urls.py              # Application URL patterns
│   ├── admin.py             # Enhanced admin interface
│   └── management/          # Custom management commands
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── accounts/           # Authentication templates
│   └── employee/           # Dashboard and form templates
├── requirements.txt         # Python dependencies
├── setup.bat               # Automated setup script
└── README.md               # This file
```

## Key Components

### Models
- **Employee**: Extends Django User with work-related fields (position, department, hire date, employer flag)
- **LeaveRequest**: Manages leave requests with approval workflow and status tracking

### Views
- **Authentication**: Login/logout with automatic role-based redirection
- **Employee Dashboard**: Personal profile, leave history, and request submission
- **Employer Dashboard**: Employee management, leave request approval, and analytics
- **Profile Management**: Update personal and work information

### Templates
- **Responsive Design**: Bootstrap 5 with custom CSS for modern appearance
- **Role-Based Navigation**: Dynamic sidebar based on user permissions
- **Interactive Forms**: Client-side validation and user feedback
- **Data Tables**: Sortable and filterable employee and leave request lists

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` using the super admin credentials:
- Enhanced employee management with inline user profiles
- Advanced leave request tracking with filters and search
- Customized admin interface with company branding

## Technical Features

### Backend
- **Django 5.2**: Latest stable version with security updates
- **Model Relationships**: Proper foreign key relationships and cascading deletes
- **Management Commands**: Custom commands for data initialization
- **Role-Based Logic**: Automatic user routing based on employee type

### Frontend
- **Bootstrap 5**: Modern CSS framework for responsive design
- **Font Awesome**: Professional icons throughout the interface
- **JavaScript**: Client-side form validation and interactive features
- **CSS Gradients**: Modern visual effects and smooth transitions

### Database
- **SQLite**: Default database for development (easily changeable)
- **Model Methods**: Custom methods for business logic (leave duration calculation)
- **Data Integrity**: Proper constraints and validation rules

## Customization

### Adding New Departments
Update the department choices in `templates/employee/profile.html`:
```html
<option value="New Department">New Department</option>
```

### Modifying Leave Approval Logic
Edit the `approve()` method in `employee/models.py` to customize approval behavior.

### Styling Changes
Modify the CSS in `templates/base.html` or create separate CSS files for custom styling.

## Future Enhancements

- 📧 Email notifications for leave request updates
- 📱 Mobile app integration
- 📊 Advanced reporting and analytics
- 🌐 Multi-language support (i18n framework already included)
- 📅 Calendar integration for leave visualization
- 🔗 API endpoints for third-party integrations

## License

This project is developed for educational and demonstration purposes. Feel free to use and modify according to your needs.

## Support

For questions or issues, please refer to the Django documentation or create an issue in the repository.

---

**Built with ❤️ using Django 5.2 and Bootstrap 5**