from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
# Employee model that extends the User model with is_employer flag
# and additional fields like position, department, and date of hire
# This model will store additional employee-specific information
# when an employee is created, a corresponding User model should also be created
# when an employee is updated, the corresponding User model should also be updated
# if an employee updates their first name, last name, or email, it should update the corresponding User model
# if an employee is deleted, the corresponding User model should also be deleted
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, default='Unknown')
    department = models.CharField(max_length=100, default='General')
    date_of_hire = models.DateField(default=now)
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"
    

# This model is used to store leave requests made by employees
# if an employee's leave request is approved, the User object associated with the request should update it's is_active status
class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.status = 'Approved'
        self.save()
        self.employee.user.is_active = False
        self.employee.user.save()

    def __str__(self):
        return f"{self.employee.user.first_name} {self.employee.user.last_name} - {self.status}"