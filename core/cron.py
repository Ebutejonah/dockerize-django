from datetime import timedelta
from django.utils import timezone
from core.models import CustomUser
from core.signals import send_subscription_reminder


def send_sub_reminder():
    # Calculate the date 28 days ago from today
    twenty_eight_days_ago = timezone.now() - timedelta(days=28)

    # Get all users who haven't paid and haven't received a reminder in the last 28 days
    users_to_remind = CustomUser.objects.filter(has_paid_this_month=False, last_reminder_sent__lt=twenty_eight_days_ago)

    # Loop through the users and send them a reminder
    for user in users_to_remind:
        send_subscription_reminder(sender=CustomUser, instance=user)
    return None

def delete_inactive_user():
    users = CustomUser.objects.filter(is_active=False)
    for user in users:
        if timezone.now() >= user.scheduled_deletion_time:
            user.delete()
    return None