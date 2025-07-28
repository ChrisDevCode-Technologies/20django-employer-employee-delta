@echo off
echo ================================
echo Employee-Employer System Setup
echo ================================

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Step 3: Creating sample data...
python manage.py create_sample_data

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Login credentials:
echo   Admin/Employer: admin / admin123
echo   HR Manager: employer / employer123
echo   Employee Example: alice_smith / password123
echo.
echo Access the application at: http://127.0.0.1:8000/
echo.
pause
