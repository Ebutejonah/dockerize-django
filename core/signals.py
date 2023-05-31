from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def schedule_deletion(sender, instance, created, **kwargs):    
    if created and not instance.is_active:
        print('We are going somewhere')
        instance.scheduled_deletion_time = timezone.now() + timezone.timedelta(minutes=1)
        print(instance.scheduled_deletion_time)
        print(instance.is_active)
        CustomUser.objects.filter(email=instance.email).update(scheduled_deletion_time=instance.scheduled_deletion_time)

    if instance.is_active:
        instance.scheduled_deletion_time = None
        CustomUser.objects.filter(email=instance.email).update(scheduled_deletion_time=instance.scheduled_deletion_time)

    

@receiver(post_save, sender=CustomUser)
def send_subscription_reminder(sender, instance, created, **kwargs):
    if created:
        #Set the last reminder sent time to the current time
        instance.last_reminder_sent = timezone.now()
        instance.save(update_fields=['last_reminder_sent'])

    #Check if it's been 30 days since the last reminder was sent
    if instance.last_reminder_sent is None or (timezone.now() - instance.last_reminder_sent) >= timedelta(days=30):
        #Check if the user has not paid this month
        if not instance.paid_for_the_month:
            # Send a reminder email
            send_mail(
                'Subscription Reminder',
                'Hello {},\n\nThis is a reminder that your subscription is due. Please make your payment as soon as possible.\n\nThank you for using our service!'.format(instance.first_name),
                'techforjonah@gmail.com',
                [instance.email],
                fail_silently=False,
            )
            #Update the last reminder sent time
            instance.last_reminder_sent = timezone.now()
            instance.save()


'''@receiver(post_save, sender = CustomUser)  
def perform_scheduled_deletion(sender,instance,*args,**kwargs):
    if not instance.is_active and timezone.now() >= instance.scheduled_deletion_time:
        print(timezone.now())
        print(instance.is_active)
        instance.delete()'''