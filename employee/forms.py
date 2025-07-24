# Create a form for employees to submit leave requests with start date, end date, and reason fields
# Form includes input fields for start date, end date, and reason.
# Form submission creates a LeaveRequest entry with status "Pending".
# Form is accessible in max 2 clicks from the dashboard.
# Tooltips/help text provided for date fields.

from django import forms
from .models import LeaveRequest
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the reason for your leave request'}),
        }
        help_texts = {
            'start_date': 'Select the start date of your leave.',
            'end_date': 'Select the end date of your leave.',
            'reason': 'Provide a detailed reason for your leave request.',
        }
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data