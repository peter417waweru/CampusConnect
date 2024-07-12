from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ApprovalRequest

@login_required
def workflow_home(request):
    return render(request, 'workflow/workflow_home.html')

@login_required
def list_requests(request):
    requests = ApprovalRequest.objects.all()
    return render(request, 'workflow/list_requests.html', {'requests': requests})

@login_required
def request_detail(request, pk):
    request = get_object_or_404(ApprovalRequest, pk=pk)
    return render(request, 'workflow/request_detail.html', {'request': request})

@login_required
def approve_request(request, pk):
    request = get_object_or_404(ApprovalRequest, pk=pk)
    request.status = 'approved'
    request.save()
    return redirect('workflow:list_requests')

@login_required
def reject_request(request, pk):
    request = get_object_or_404(ApprovalRequest, pk=pk)
    request.status = 'rejected'
    request.save()
    return redirect('workflow:list_requests')
