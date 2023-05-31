from django.shortcuts import render, redirect
from .models import CustomUser, Payments
from .forms import  CustomUserCreationForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django_email_verification import send_email
from django.utils import timezone
from datetime import timedelta



'''def registerview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.info(request, 'Passwords must match. Kindly fill form again.')
            return redirect('/register')
        elif len(password) < 8:
            messages.info(request, 'Password must have at least 8 characters.')
            return redirect('/register')
        elif CustomUser.objects.filter(email = email).exists():
            messages.info(request, 'An account with the email you provided already exists. Please go to Login Page')
            return redirect('/register')
        else:
            user = CustomUser.objects.create_user(email=email,password=password)
            user.save()
            profile = Profile.objects.create(user=user,email=email)
            profile.save()

            #sending Welcome email to registered user
            template = render_to_string('core/welcome.html',{'email':email})
            send_email = EmailMessage(
                'Welcome to My Project Demo',
                template,
                settings.EMAIL_HOST_USER,
                [email]
            )
            send_email.fail_silently = False
            send_email.send()

            return redirect('/')
    return render(request, 'index.html')'''

def registerview(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(user)
            #sending Welcome email to registered user
            '''email = form.cleaned_data.get('email')
            template = render_to_string('core/welcome.html',{'email':email})
            send_mail = EmailMessage(
                'Welcome to My Project Demo',
                template,
                settings.EMAIL_HOST_USER,
                [email]
            )
            send_mail.fail_silently = False
            send_mail.send()'''
            return redirect('/registered')
    else:
        form = CustomUserCreationForm()

    return render(request, 'index.html', {'form': form})

def registeredview(request):
    return render(request, 'registered.html')


def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
            if password != user.password:
                messages.info(request, 'Invalid Email or Password')
        except:
            CustomUser.DoesNotExist()
            messages.info(request, 'Invalid Email or Password')
        account = auth.authenticate(email=email,password=password)
        if account is not None:
            auth.login(request,user)
            return redirect('/checkout')
    return render(request, 'login.html')



@login_required()
def dashboardview(request):
    '''form = ProfileForm()
    email = request.user.email
    user = CustomUser.objects.get(email = email)
    profile = Profile.objects.get(user = user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('/checkout')
        else:
            messages.info(request,'Please enter a valid phone number')
        return redirect('/dashboard')
    context = {'user':user,'profile':profile,'form':form}
    return render(request, 'dashboard.html',context)'''
    return HttpResponse( 'dashboard')

@login_required()
def logoutview(request):
    auth.logout(request)
    return redirect('/')

@login_required()
def checkoutview(request):
    email = request.user.email
    user = CustomUser.objects.get(email = email)
    payment = Payments.objects.create(user=user)
    context= {'user':user,'payment':payment}
    return render(request,'checkout.html',context)

@login_required()
def successpage(request,id):
    email = request.user.email
    user = CustomUser.objects.get(email = email)
    user.paid_for_the_month = True
    payment = Payments.objects.get(uuid=id)
    payment.paid_for_the_month = True
    payment.save()
    messages.success(request, 'Payment made successfully')
    return redirect('/checkout')