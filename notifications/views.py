from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    """
    Show all notifications for the logged-in user.
    Auto mark all as read on visit.
    """
    notifications = Notification.objects.filter(user=request.user)

    # auto mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
    })