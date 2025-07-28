from django import forms
from .models import LeaveRequest

class LeaveRequestFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + LeaveRequest.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search employee name or ID'})
    )