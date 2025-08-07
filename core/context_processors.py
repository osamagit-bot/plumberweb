def admin_notifications(request):
    """Add unread notification count to admin context"""
    if request.path.startswith('/admin/'):
        try:
            from core.models import AdminNotification
            unread_count = AdminNotification.objects.filter(is_read=False).count()
            return {'unread_notifications_count': unread_count}
        except:
            return {'unread_notifications_count': 0}
    return {}