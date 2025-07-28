from django.urls import path
from . import views

app_name = 'employer'

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='dashboard'),
    path('leave-requests/', views.leave_requests_list, name='leave_requests_list'),
    path('leave-requests/<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('leave-requests/<int:pk>/approve/', views.approve_leave_request, name='approve_leave_request'),
    path('leave-requests/<int:pk>/reject/', views.reject_leave_request, name='reject_leave_request'),
]