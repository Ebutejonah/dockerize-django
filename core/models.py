from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import uuid



class UserModelManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        '''Create and save a User with the given email and password'''
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password=None, **extra_fields):
        '''Create and save a Superuser with the given email and password'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self._create_user(email,password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=250,null=True,blank=True)
    paid_for_the_month = models.BooleanField(default=False,blank=True,null=True)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    scheduled_deletion_time = models.DateTimeField(null=True, blank=True, default=None)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserModelManager()



'''class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=250,null=True,blank=True)
    paid_for_the_month = models.BooleanField(default=False,blank=True,null=True)
    registration_date = models.DateTimeField(default = datetime.now,blank=True, null=True)

    def __str__(self):
        return self.user.email
    
    @receiver(post_save, sender=CustomUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_profile, sender=CustomUser)'''
    
class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    paid = models.BooleanField(default=False)
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False,null=True, blank=True)
    due_date = models.DateTimeField(auto_now_add=True)
    paid_for_the_month = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return self.profile.email + " payments"