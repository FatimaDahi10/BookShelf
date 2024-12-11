from notifications.models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': Notification.objects.filter(recipient=request.user, unread=True).count()
        }
    return {}
