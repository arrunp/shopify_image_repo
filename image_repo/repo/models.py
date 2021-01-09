from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    imageName = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    vision_tags = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class History(models.Model):
    uploaded = 'uploaded'
    deleted = 'ueleted'
    STATUS_CHOICES = [
        (uploaded, 'uploaded'),
        (deleted, 'ueleted'),
    ]

    user = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    action = models.CharField(max_length=8, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now=True)
