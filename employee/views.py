from django.contrib import messages
from django.shortcuts import redirect, render

from employee.forms import LeaveRequestForm
from employee.models import Employee, LeaveRequest

def index_view(request):
    """
    Render the employee index page.
    """
    # Get the employee and leave instance
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        employee = Employee.objects.get(user=request.user)
        leave_requests = LeaveRequest.objects.filter(employee=employee)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('profile')


    # Initialize the leave request form
    form = LeaveRequestForm()

    # if the user posts the form, save the leave request
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = employee
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('employee:dashboard')  # Adjust to your url name if different

    return render(request, 'employee/index.html', {'employee': employee, 'form': form, 'leave_requests': leave_requests})

#         # Calculate statistics
#         total_employees = employees.count()
#         total_requests = leave_requests.count()
#         pending_count = pending_requests.count()
#         approved_count = leave_requests.filter(status='Approved').count()
#         rejected_count = leave_requests.filter(status='Rejected').count()
        
#         context = {
#             'employees': employees,
#             'leave_requests': leave_requests,
#             'pending_requests': pending_requests,
#             'total_employees': total_employees,
#             'total_requests': total_requests,
#             'pending_count': pending_count,
#             'approved_count': approved_count,
#             'rejected_count': rejected_count,
#         }
        
#         return render(request, 'employee/employer_dashboard.html', context)
#     except Employee.DoesNotExist:
#         messages.error(request, 'Employee profile not found.')
#         return redirect('login')


# @login_required
# def manage_leave_request(request, request_id):
#     """Handle leave request approval/rejection"""
#     try:
#         current_employee = Employee.objects.get(user=request.user)
        
#         # Check if user is an employer
#         if not current_employee.is_employer:
#             messages.error(request, 'Access denied. You are not authorized to perform this action.')
#             return redirect('employee_dashboard')
        
#         leave_request = get_object_or_404(LeaveRequest, id=request_id)
        
#         if request.method == 'POST':
#             action = request.POST.get('action')
            
#             if action == 'approve':
#                 leave_request.status = 'Approved'
#                 leave_request.save()
#                 messages.success(request, f'Leave request for {leave_request.employee.user.get_full_name()} has been approved.')
#             elif action == 'reject':
#                 leave_request.status = 'Rejected'
#                 leave_request.save()
#                 messages.success(request, f'Leave request for {leave_request.employee.user.get_full_name()} has been rejected.')
        
#         return redirect('employer_dashboard')
#     except Employee.DoesNotExist:
#         messages.error(request, 'Employee profile not found.')
#         return redirect('login')
#lkjgdk