from django.urls import path
from .views import registeredview, registerview, loginview, dashboardview, logoutview, checkoutview
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', loginview, name="login"),
    path('register/', registerview, name="register"),
    path('dashboard/', dashboardview, name="dashboard"),
    path('logout/', logoutview, name="logout"),
    path('checkout/', checkoutview, name="checkout"),
    path('registered/', registeredview, name='registered'),
    
    #password change and reset
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name = 'registration/password_change.html'), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'registration/password_changed.html'), 
        name='password_change_done'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/reset_email.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/reset_complete.html'),
     name='password_reset_complete'),


]