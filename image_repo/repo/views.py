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
# Create your views here.

current_image_name = None

# View to create new image upload
# @params for this class is CreateView, a django view that displays a form for creating an object and saving it
#         - The field 'model' is Image, as this form will be creating an Image object
#         - The fields included on the form based on the Image model are 'title', 'image', and 'tags' (please refer to models.py
#         to see the types for these fields)
#         - template name is the name where the form to generate the object will be displayed (index.html)
#         - success_url takes the object returned from reverse_lazy('home'), 'home' being the name of the home page's url
#         to return the user to this page once the form is successfully submitted
# @return  The image object submitted from the form will be saved based on the Image model.


class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'repo/index.html'
    success_url = reverse_lazy('home')

    # If the Google Vision API credentials are provided, image_detect will use the API to provide tag suggestions
    # for an image based on object detection. If the credentials are not provided it will use the python cvlib for
    # providing these object detection suggestions
    # @params image_url: the url of the image that the object detection will be run on
    # @returns suggested_vision_tags: a string of suggested tags for the image based on objects detected in it
    def image_detect(self, image_url):

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

        client = vision.ImageAnnotatorClient()

        labels = []
        label_string = ""

        image = types.Image()
        image.source.image_uri = image_url

        response_label = client.label_detection(image=image)

        for label in response_label.label_annotations:
            labels.append(label.description)

        for label in labels:
            if len(label.split()) == 1:
                label_string += label + ", "

        suggested_vision_tags = label_string.strip(', ')
        return suggested_vision_tags

    # 1) checks if image being uploaded through the form has the same name as a file already uploaded
    # 2) updates the imageName field in the database of the image being uploaded with the (new) name of the image
    #    (django changes the name of the image if there are duplicates, this imageName field keeps track of
    #    that in the DB)
    # @params form: the current form (CreateView)
    # @returns saves the form instance and redirects to the success_url by default
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

    # The context data is provided to the rendered template at the success_url upon successful submission of the form
    # @params **kwargs: a dictionary of keyword arguments
    # @returns The context data (a dictionary of values) will be returned and sent to the success url.
    #          Context has the stored images (context['images'] and the name of the image that was just created
    #          using the CreateView form context['current_image_name']. The images are held in context in chronologial
    #          order (latest stored images first)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all().order_by('-date')
        context['images'] = images
        global current_image_name
        context['current_image_name'] = current_image_name
        current_image_name = None
        return context

# Used to search for images that match the search criteria (searches image title, name and tags)
# @params request: takes in the GET request provided by the search form in index.html.
#                  Depending on if the vision_tag_search checkbox is checked or not, the suggested tags
#                  provided by the Google Vision API may or may not be included in the search (checked = include
#                  Google Vision API suggestions)
# @returns an HttpResponse which renders a template (index.html) with a provided dictionary of values
#          (this dictionary has one key, found_images, which contains the images that match the search criteria a
#           and this data is sent to be on the rendered index.html)


def imageSearch(request):
    if request.method == 'GET':
        search = request.GET.get('imageSearch')
        vision_tag_search = request.GET.get('vision_tag_search')
        unique_images = set()
        search = search.split(" ")

        images = Image.objects.all()
        for word in search:
            for image in images:
                # Searching based on user inputted tags
                if image.tags != None:
                    tags_list = []
                    for x in image.tags.split(','):
                        tags_list.append(x.strip().lower())
                    if word.lower() in tags_list:
                        unique_images.add(image)
                # Searching based on suggested tags provided by google vision api
                if vision_tag_search == 'on':
                    if image.vision_tags != None:
                        vision_tags_list = []
                        for x in image.vision_tags.split(','):
                            vision_tags_list.append(x.strip().lower())
                        if word.lower() in vision_tags_list:
                            unique_images.add(image)

        # Searching based on titles and imageName field
        for word in search:
            found_images = Image.objects.filter(
                Q(title__icontains=word) | Q(imageName__icontains=word)
            ).distinct()

            for image in found_images:
                unique_images.add(image)

        # In the case the images showed up in more than one search criteria, they were stored in a set and are
        # now being converted to a list.
        unique_images = list(unique_images)

        return render(request, 'repo/search.html', {'found_images': unique_images[::-1]})

# Deletes image row in DB based on ID and deletes image in S3 bucket
# @params request: takes in the POST request provided by the delete form in index.html
#         **kwargs: keyword arguments provided by the url
# @returns an HttpResponse which leads back to a template (index.html) after performing the operation of
#          deleting the item in the db which has the matching ID provided by the 'pk' key word argument parameter.
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
