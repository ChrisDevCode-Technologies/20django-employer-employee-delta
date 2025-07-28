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
        return redirect('dashboard')


    # Initialize the leave request form
    form = LeaveRequestForm()

    # if the user posts the form, save the leave request
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = employee
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('employee:index')  # Adjust to your url name if different

    return render(request, 'employee/index.html', {'employee': employee, 'form': form, 'leave_requests': leave_requests})