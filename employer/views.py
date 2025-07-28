from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import LeaveRequest, Employee


@login_required
def employer_dashboard(request):
    """Main employer dashboard showing leave request statistics"""
    if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
        messages.error(request, "Access denied. You don't have employer privileges.")
        return redirect('home')
    
    # Get statistics
    total_requests = LeaveRequest.objects.count()
    pending_requests = LeaveRequest.objects.filter(status='pending').count()
    approved_requests = LeaveRequest.objects.filter(status='approved').count()
    rejected_requests = LeaveRequest.objects.filter(status='rejected').count()
    
    # Recent requests
    recent_requests = LeaveRequest.objects.select_related('employee__user').order_by('-created_at')[:5]
    
    context = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'recent_requests': recent_requests,
    }
    return render(request, 'employer/dashboard.html', context)

@login_required
def leave_requests_list(request):
    """View all leave requests with filtering and pagination"""
    if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
        messages.error(request, "Access denied. You don't have employer privileges.")
        return redirect('home')
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    department_filter = request.GET.get('department', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    leave_requests = LeaveRequest.objects.select_related('employee__user', 'approved_by__user')
    
    # Apply filters
    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter)
    
    if department_filter:
        leave_requests = leave_requests.filter(employee__department=department_filter)
    
    if search_query:
        leave_requests = leave_requests.filter(
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__employee_id__icontains=search_query) |
            Q(reason__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(leave_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique departments for filter dropdown
    departments = Employee.objects.values_list('department', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'search_query': search_query,
        'departments': departments,
        'status_choices': LeaveRequest.STATUS_CHOICES,
    }
    return render(request, 'employer/leave_requests_list.html', context)

@login_required
def leave_request_detail(request, pk):
    """View detailed information about a specific leave request"""
    if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
        messages.error(request, "Access denied. You don't have employer privileges.")
        return redirect('home')
    
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    context = {
        'leave_request': leave_request,
    }
    return render(request, 'employer/leave_request_detail.html', context)

@login_required
@require_POST
def approve_leave_request(request, pk):
    """Approve a leave request"""
    if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave_request.status != 'pending':
        return JsonResponse({'success': False, 'error': 'Leave request is not pending'})
    
    leave_request.status = 'approved'
    leave_request.approved_by = request.user.employee
    leave_request.approved_at = timezone.now()
    leave_request.save()
    
    messages.success(request, f'Leave request for {leave_request.employee} has been approved.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': 'Leave request approved successfully',
            'new_status': 'approved'
        })
    
    return redirect('leave_request_detail', pk=pk)

@login_required
@require_POST
def reject_leave_request(request, pk):
    """Reject a leave request"""
    if not hasattr(request.user, 'employee') or not request.user.employee.is_employer:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if leave_request.status != 'pending':
        return JsonResponse({'success': False, 'error': 'Leave request is not pending'})
    
    leave_request.status = 'rejected'
    leave_request.approved_by = request.user.employee
    leave_request.approved_at = timezone.now()
    leave_request.save()
    
    messages.success(request, f'Leave request for {leave_request.employee} has been rejected.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': 'Leave request rejected successfully',
            'new_status': 'rejected'
        })
    
    return redirect('leave_request_detail', pk=pk)