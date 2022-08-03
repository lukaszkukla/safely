from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Hazard(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Risk(models.Model):
    level = models.CharField(max_length=6, unique=True, default='Low')

    def __str__(self):
        return self.level

    class Meta:
        verbose_name_plural = 'Risks'


class Status(models.Model):
    name = models.CharField(max_length=8, unique=True, default='Open')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Statuses'

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15, null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()