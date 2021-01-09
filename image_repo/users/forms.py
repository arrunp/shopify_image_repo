from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# The fields listed here are the fields that will be listed on the
# user creation form. This class adds the email field to the form


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
