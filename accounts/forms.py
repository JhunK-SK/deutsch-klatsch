from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from allauth.account.forms import SignupForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, 
        help_text='Required, Enter avalid Email address.'
    )
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password1', 'password2']
        
# This is for admin page.
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']
    
    
class CustomUserProfileForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ['avatar',]
        widgets = {
            'avatar': forms.FileInput,
        }
        
        
        
# since using django-allauth, this form is not necessary anymore.
# unless I customise allauth-loginForm with this CustomUserAuthenticationForm
# class CustomUserAuthenticationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
#     class Meta:
#         model   = get_user_model()
#         fields  = ['email', 'password']
        
#     def clean(self):
#         email       = self.cleaned_data['email']
#         password    = self.cleaned_data['password']
#         if not authenticate(email=email, password=password):
#             raise forms.ValidationError('Invalid login man')