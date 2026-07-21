from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    A message sent to a user.
    Created by other apps when something important happens.
    Example: Notification.objects.create(user=player, message="You were approved!")
    """

    # who receives this notification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',   # user.notifications.all()
    )

    # the message text shown to the user
    message = models.TextField()

    # False = not seen yet, True = user has read it
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest notifications come first
        ordering = ['-created_at']

    def __str__(self):
        status = "read" if self.is_read else "unread"
        return f"To {self.user.username}: {self.message[:40]} [{status}]"