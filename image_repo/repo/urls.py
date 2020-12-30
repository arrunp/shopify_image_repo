from django.urls import path
from . import views
from .views import ImageCreateView, ImageListView

urlpatterns = [
    path('', ImageListView.as_view(), name="home"),
    path('create/', ImageCreateView.as_view(), name="create"),
]
