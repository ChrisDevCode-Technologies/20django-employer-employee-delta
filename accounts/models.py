from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extended user profile to distinguish between employers and employees.
    """

    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('employee', 'Employee'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='employee'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    address = models.TextField(
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

def __str__(self):
    username = self.user.username if self.user else "Unknown User"
    return f"{username}'s Profile - {self.role}"
