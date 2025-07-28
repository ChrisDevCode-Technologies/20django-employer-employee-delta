from django.contrib import admin
from .models import Employee, LeaveRequest


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'position', 'department', 'date_of_hire', 'is_employer']
    list_filter = ['department', 'is_employer', 'date_of_hire']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'position', 'department']
    ordering = ['user__first_name', 'user__last_name']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['get_employee_name', 'start_date', 'end_date', 'get_duration', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'created_at', 'employee__department']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'reason']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def get_employee_name(self, obj):
        return obj.employee.user.get_full_name() or obj.employee.user.username
    get_employee_name.short_description = 'Employee'
    
    def get_duration(self, obj):
        duration = (obj.end_date - obj.start_date).days + 1
        return f"{duration} day{'s' if duration > 1 else ''}"
    get_duration.short_description = 'Duration'


# Customize admin site headers
admin.site.site_header = "Employer-Employee System Admin"
admin.site.site_title = "EES Admin"
admin.site.index_title = "Welcome to EES Administration"