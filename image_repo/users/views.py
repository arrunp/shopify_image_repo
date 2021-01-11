from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from repo.models import Image
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Creating a user registration form that is going to be passed to the HTML template
# Django handles validation checks (ex. passwords match, valid email, correct types of information for fields
# are being inputted) through the UserCreationForm(). This form is treated as a class that will be converted into
# the HTML template.
# @params request: takes in the POST request provided by the form in register.html
# @returns the form created is passed to the template (register.html) to create a new user


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to login')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

#


def archive(request, **kwargs):

    if request.method == 'POST':
        if request.POST.get('imageArchive'):
            if request.user.is_authenticated:
                image = Image.objects.filter(id=kwargs['pk']).first()
                if request.user == image.uploader:
                    if image.archived == False:
                        image.archived = True
                        image.save()
                    else:
                        image.archived = False
                        image.save()
                else:
                    messages.warning(
                        request, f'You cannot archive images you did not upload.')
            else:
                messages.warning(
                    request, f'You cannot archive images you did not upload.')
                return redirect('login')

            return HttpResponseRedirect(reverse('home'))


@login_required
def viewArchive(request):
    archived_images = Image.objects.filter(
        uploader=request.user).filter(archived=True)

    return render(request, 'users/archive.html', {'archived_images': archived_images})
