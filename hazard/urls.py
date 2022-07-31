from django.urls import path
from .views import HazardList, HazardDetail


urlpatterns = [
    path('', HazardList.as_view(), name='hazards'),
    path('hazard/<int:pk>/', HazardDetail.as_view(), name='hazard'),
]