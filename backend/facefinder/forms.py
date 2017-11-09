#log/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django import forms
from django.forms import EmailField
from django.forms import PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# My imports
from .models import Video

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    firstname = forms.CharField(label="", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name','placeholder': 'First Name (Optional)'}))
    lastname = forms.CharField(label="", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name','placeholder': 'Last Name (Optional)'}))
    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username','placeholder': 'Username'}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password','placeholder': 'Password'}))

class SignUpForm(UserCreationForm):
    firstname = forms.CharField(label="", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name','placeholder': 'First Name (optional)'}))
    lastname = forms.CharField(label="", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name','placeholder': 'Last Name (optional)'}))
    username = EmailField(label=(""), required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email','placeholder': 'Email Address'}))
    password1 = forms.CharField(label="",
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1','placeholder': 'Create a password'}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2','placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'password1', 'password2')

class NewVideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('video', )
