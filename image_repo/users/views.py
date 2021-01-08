from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

# Creating a user registration form that is going to be passed to the HTML template
# Django handles validation checks (ex. passwords match, valid email, correct types of information for fields
# are being inputted) through the UserCreationForm(). This form is treated as a class that will be converted into
# the HTML template
# @returns: the form created is passed to the template (register.html) to create a new user


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for \'{username}\'!')
            return redirect('home')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
