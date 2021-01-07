from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    imageName = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    vision_tags = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
