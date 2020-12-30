from django.shortcuts import render, redirect
#from .form import ImageForm
from .models import Image
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy


# Create your views here.
class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'repo/create_image.html'
    success_url = reverse_lazy('home')


class ImageListView(ListView):
    model = Image
    template_name = 'repo/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all().order_by('-date')
        context['images'] = images

        return context
