from django.db import models

# Create your models here.


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    imageName = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
