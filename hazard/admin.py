from django.contrib import admin
from .models import Hazard, Category, Risk, Status  

admin.site.register(Hazard)
admin.site.register(Category)
admin.site.register(Risk)
admin.site.register(Status)
# admin.site.register(UserProfile)