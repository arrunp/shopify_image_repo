from django.urls import path
from . import views
from .views import ImageCreateView

urlpatterns = [
    path('', ImageCreateView.as_view(), name="home"),
]
