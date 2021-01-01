from django.db import models
from django.dispatch import receiver
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from .form import ImageForm
from .models import Image
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import boto3
from django.conf import settings


# Create your views here.
class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'repo/index.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all().order_by('-date')
        context['images'] = images

        return context


def imageSearch(request):
    if request.method == 'GET':
        search = request.GET.get('imageSearch')
        queryset = []
        search = search.split(" ")

        for word in search:
            found_images = Image.objects.filter(
                Q(title__icontains=word) | Q(
                    tags__icontains=word)
            ).distinct()

            for image in found_images:
                queryset.append(image)

        return render(request, 'repo/index.html', {'found_images': queryset[::-1]})


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
