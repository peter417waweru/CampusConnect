from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, SupportTicket
from .forms import FeedbackForm, SupportTicketForm

@login_required
def support_home(request):
    return render(request, 'support/support_home.html')

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('support:list_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'support/submit_feedback.html', {'form': form})

@login_required
def list_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'support/list_feedback.html', {'feedbacks': feedbacks})

@login_required
def support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('support:list_tickets')
    else:
        form = SupportTicketForm()
    return render(request, 'support/support_ticket.html', {'form': form})

@login_required
def list_tickets(request):
    tickets = SupportTicket.objects.all()
    return render(request, 'support/list_tickets.html', {'tickets': tickets})
