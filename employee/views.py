from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Employee, LeaveRequest
from django.utils import timezone
from datetime import datetime


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if user is an employer or employee and redirect accordingly
            try:
                employee = Employee.objects.get(user=user)
                if employee.is_employer:
                    return redirect('employer_dashboard')
                else:
                    return redirect('employee_dashboard')
            except Employee.DoesNotExist:
                messages.error(request, 'Employee profile not found.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def employee_dashboard(request):
    """Employee dashboard showing profile and leave requests"""
    try:
        employee = Employee.objects.get(user=request.user)
        
        # Get employee's leave requests
        leave_requests = LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
        
        # Calculate some statistics
        pending_requests = leave_requests.filter(status='Pending').count()
        approved_requests = leave_requests.filter(status='Approved').count()
        rejected_requests = leave_requests.filter(status='Rejected').count()
        
        context = {
            'employee': employee,
            'leave_requests': leave_requests,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'rejected_requests': rejected_requests,
        }
        
        return render(request, 'employee/dashboard.html', context)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')


@login_required
def submit_leave_request(request):
    """Handle leave request submission"""
    try:
        employee = Employee.objects.get(user=request.user)
        
        if request.method == 'POST':
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            reason = request.POST['reason']
            
            # Convert string dates to date objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Validate dates
            if start_date >= end_date:
                messages.error(request, 'End date must be after start date.')
                return render(request, 'employee/submit_leave.html')
            
            if start_date <= timezone.now().date():
                messages.error(request, 'Start date must be in the future.')
                return render(request, 'employee/submit_leave.html')
            
            # Create leave request
            LeaveRequest.objects.create(
                employee=employee,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('employee_dashboard')
        
        return render(request, 'employee/submit_leave.html')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')


@login_required
def employer_dashboard(request):
    """Employer dashboard showing all employees and leave requests"""
    try:
        current_employee = Employee.objects.get(user=request.user)
        
        # Check if user is an employer
        if not current_employee.is_employer:
            messages.error(request, 'Access denied. You are not authorized to view this page.')
            return redirect('employee_dashboard')
        
        # Get all employees
        employees = Employee.objects.all().order_by('user__first_name')
        
        # Get all leave requests
        leave_requests = LeaveRequest.objects.all().order_by('-created_at')
        
        # Get pending leave requests
        pending_requests = LeaveRequest.objects.filter(status='Pending').order_by('-created_at')
        
        # Calculate statistics
        total_employees = employees.count()
        total_requests = leave_requests.count()
        pending_count = pending_requests.count()
        approved_count = leave_requests.filter(status='Approved').count()
        rejected_count = leave_requests.filter(status='Rejected').count()
        
        context = {
            'employees': employees,
            'leave_requests': leave_requests,
            'pending_requests': pending_requests,
            'total_employees': total_employees,
            'total_requests': total_requests,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
        }
        
        return render(request, 'employee/employer_dashboard.html', context)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')


@login_required
def manage_leave_request(request, request_id):
    """Handle leave request approval/rejection"""
    try:
        current_employee = Employee.objects.get(user=request.user)
        
        # Check if user is an employer
        if not current_employee.is_employer:
            messages.error(request, 'Access denied. You are not authorized to perform this action.')
            return redirect('employee_dashboard')
        
        leave_request = get_object_or_404(LeaveRequest, id=request_id)
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'approve':
                leave_request.status = 'Approved'
                leave_request.save()
                messages.success(request, f'Leave request for {leave_request.employee.user.get_full_name()} has been approved.')
            elif action == 'reject':
                leave_request.status = 'Rejected'
                leave_request.save()
                messages.success(request, f'Leave request for {leave_request.employee.user.get_full_name()} has been rejected.')
        
        return redirect('employer_dashboard')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')


@login_required
def employee_profile(request):
    """Display and edit employee profile"""
    try:
        employee = Employee.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Update user fields
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            
            # Update employee fields
            employee.position = request.POST.get('position', employee.position)
            employee.department = request.POST.get('department', employee.department)
            employee.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('employee_profile')
        
        context = {
            'employee': employee,
        }
        
        return render(request, 'employee/profile.html', context)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('login')
