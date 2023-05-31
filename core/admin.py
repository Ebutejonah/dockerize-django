from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _



class  CustomUserAdmin(UserAdmin):
    '''Define admin model for custom User model with no username field.'''
    fieldsets = (
        (None, {'fields': ('email', 'password','address','phone_number','paid_for_the_month','last_reminder_sent','scheduled_deletion_time')}),
        (_('Personal info'),{'fields':('first_name', 'last_name')}),
        (_('Permissions'),{'fields':('is_active', 'is_staff','is_superuser','groups','user_permissions')}),
        (_('Important dates'),{'fields':('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields':('email','password','password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(get_user_model(), CustomUserAdmin)
