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
from google.cloud import vision
from google.cloud.vision_v1 import types
import os
import json
# Create your views here.

current_image_name = None

# View to create new image upload


class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'repo/index.html'
    success_url = reverse_lazy('home')

    def image_detect(self, image_url):

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'probable-quest-242019-805cd1d7f139.json'

        client = vision.ImageAnnotatorClient()

        labels = []
        label_string = ""

        image = types.Image()
        image.source.image_uri = image_url

        response_label = client.label_detection(image=image)

        for label in response_label.label_annotations:
            labels.append(label.description)

        for label in labels:
            label_string += label + ", "

        return label_string.strip(',')

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
        current_image.vision_tags = self.image_detect(current_image.image.url)
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
# @params request: takes in the GET request provided by the search form in index.html
# @returns an HttpResponse which renders a template (index.html) with a provided dictionary of values
#          (in this case with the one key, found_images) - founded images contains the images that match
#          the search criteria and displays it on the rendered index.html


def imageSearch(request):
    if request.method == 'GET':
        search = request.GET.get('imageSearch')
        vision_tag_search = request.GET.get('vision_tag_search')
        unique_images = set()
        search = search.split(" ")

        images = Image.objects.all()
        for word in search:
            for image in images:
                if image.tags != None:
                    tags_list = []
                    for x in image.tags.split(','):
                        tags_list.append(x.strip().lower())
                    if word.lower() in tags_list:
                        unique_images.add(image)

        if vision_tag_search == 'on':
            for word in search:
                for image in images:
                    if image.vision_tags != None:
                        vision_tags_list = []
                        for x in image.vision_tags.split(','):
                            vision_tags_list.append(x.strip().lower())
                        if word.lower() in vision_tags_list:
                            unique_images.add(image)

        for word in search:
            found_images = Image.objects.filter(
                Q(title__icontains=word) | Q(imageName__icontains=word)
            ).distinct()

            for image in found_images:
                unique_images.add(image)

        unique_images = list(unique_images)

        return render(request, 'repo/index.html', {'found_images': unique_images[::-1]})

# deletes image row based on ID from db and deletes image in S3 bucket
# @params request: takes in the POST request provided by the delete form in index.html
#         **kwargs: keyword arguments provided by the url
# @returns an HttpResponse which leads back to a template (index.html) after performing the operation of
#          deleting the item in the db which has the matching ID provided by the 'pk' key word argument parameter
#          If AWS S3 is being used and an AWS_ACCESS_KEY_ID (and other necessary credentials are provided), the
#          image with the matching image URL in the S3 bucket will be deleted


def imageDelete(request, **kwargs):
    if request.method == 'POST':
        if request.POST.get('imageDelete'):

            image_id = Image.objects.filter(
                id=kwargs['pk']).first().id

            try:
                session = boto3.Session(
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                s3 = session.resource('s3')

                s3.Object(settings.AWS_STORAGE_BUCKET_NAME,
                          'media/' + Image.objects.filter(
                              id=kwargs['pk']).first().image.name).delete()

            except AttributeError:
                pass

            Image.objects.filter(id=image_id).first().delete()

        return HttpResponseRedirect(reverse('home'))
