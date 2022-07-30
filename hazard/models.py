from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Hazard(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(
        'Risk', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(
        'Status', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status', 'created_on']

class Category(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

class Risk(models.Model):
    level = models.CharField(max_length=5, unique=True, default=0)

    def __str__(self):
        return self.level

class Status(models.Model):
    name = models.CharField(max_length=8, unique=True, default=0)

    def __str__(self):
        return self.name

