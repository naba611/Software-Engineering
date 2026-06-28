from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, "Admin access only.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    players    = CustomUser.objects.filter(role='player')
    organizers = CustomUser.objects.filter(role='organizer')

    return render(request, 'dashboard/admin_dashboard.html', {
        'players':    players,
        'organizers': organizers,
    })