from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from .form import ImageForm
from .models import Image
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Q


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

            Image.objects.filter(id=image_id).first().delete()

    # doesnt work return render(request, 'repo/index.html')

        # doesnt work return reverse_lazy('home')

        return HttpResponseRedirect(reverse('home'))
