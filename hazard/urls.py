from django.urls import path
from .views import HazardList


urlpatterns = [
    path('', HazardList.as_view(), name='hazards'),
]