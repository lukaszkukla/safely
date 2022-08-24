from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Hazard(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=80)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField(null=True, blank=True)
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
        verbose_name_plural = 'Hazards'


class Category(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Risk(models.Model):
    level = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.level

    class Meta:
        verbose_name_plural = 'Risks'
        ordering = ['id']


class Status(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Statuses'
        ordering = ['id']
        