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
from models import Video

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class SignUpForm(UserCreationForm):
    username = EmailField(label=_("Email address"), required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    password1 = forms.CharField(label="Password",
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1'}))
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class NewVideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('video', )