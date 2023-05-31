from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


'''class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial = 'NG')
    )
    class Meta:
        model = Profile
        exclude = ('user', 'email','paid_for_the_month','registration_date')'''


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial = 'NG')
    )
    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name','phone_number','address')

    email = forms.EmailField(label='Email', max_length=255)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user