from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('submit-leave/', views.submit_leave_request, name='submit_leave'),
    path('manage-leave/<int:request_id>/', views.manage_leave_request, name='manage_leave'),
    path('profile/', views.employee_profile, name='employee_profile'),
]
