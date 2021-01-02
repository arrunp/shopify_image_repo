from django.db import models
from django.dispatch import receiver
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Image
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.

current_image_name = None

# View to create new image upload


class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'repo/index.html'
    success_url = reverse_lazy('home')

    # 1) checks if image being uploaded has the same name as a file already uploaded
    # 2) updates imageName field of image with the name of the image file
    def form_valid(self, form):
        send_warning = False
        current_image = form.save(commit=False)
        prev_name = current_image.image.name
        if Image.objects.filter(imageName=prev_name).first():
            send_warning = True

        images = Image.objects.all()
        current_image.save()
        current_image.imageName = current_image.image.name
        current_image.save()

        if send_warning == True:
            global current_image_name
            current_image_name = current_image.imageName

        return super(ImageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all().order_by('-date')
        context['images'] = images
        global current_image_name
        context['current_image_name'] = current_image_name
        current_image_name = None
        return context

# used to search for images that match the search criteria (searches image title, name and tags)


def imageSearch(request):
    if request.method == 'GET':
        search = request.GET.get('imageSearch')
        queryset = []
        search = search.split(" ")

        images = Image.objects.all()
        for word in search:
            for image in images:
                tags_list = []
                for x in image.tags.split(','):
                    tags_list.append(x.strip().lower())
                if word.lower() in tags_list:
                    queryset.append(image)

        for word in search:
            found_images = Image.objects.filter(
                Q(title__icontains=word) | Q(imageName__icontains=word)
            ).distinct()

            for image in found_images:
                queryset.append(image)

        return render(request, 'repo/index.html', {'found_images': queryset[::-1]})

# deletes images and deletes image in S3 bucket


def imageDelete(request, **kwargs):
    if request.method == 'POST':
        if request.POST.get('imageDelete'):

            image_id = Image.objects.filter(
                id=kwargs['pk']).first().id

            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            s3 = session.resource('s3')

            s3.Object(settings.AWS_STORAGE_BUCKET_NAME,
                      'media/' + Image.objects.filter(
                          id=kwargs['pk']).first().image.name).delete()
            Image.objects.filter(id=image_id).first().delete()

        return HttpResponseRedirect(reverse('home'))
