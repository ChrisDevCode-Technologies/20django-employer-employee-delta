from django.contrib import admin
from .models import Employee, LeaveRequest

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'position', 'is_employer']
    list_filter = ['department', 'is_employer']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'leave_type', 'created_at', 'employee__department']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee__user', 'approved_by__user')

# middleware.py (optional - for additional RBAC security)
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class EmployerAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if accessing employer URLs
        if request.path.startswith('/employer/'):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
                messages.error(request, "Access denied. You don't have employer privileges.")
                return redirect('home')
        
        response = self.get_response(request)
        return response