from django.urls import path
from .views import HazardList, HazardDetail, HazardCreate


urlpatterns = [
    path('', HazardList.as_view(), name='hazards'),
    path('hazard/<int:pk>/', HazardDetail.as_view(), name='hazard'),
    path('hazard-create/', HazardCreate.as_view(), name='hazard-create'),
]