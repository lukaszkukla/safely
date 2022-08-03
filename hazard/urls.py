from django.urls import path
from .views import (
    HazardList,
    HazardDetail,
    HazardCreate,
    HazardUpdate,
    HazardDelete,
    CustomLoginView,
    Register
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='hazards'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('', HazardList.as_view(), name='hazards'),
    path('hazard/<int:pk>/', HazardDetail.as_view(), name='hazard'),
    path('hazard-create/', HazardCreate.as_view(), name='hazard-create'),
    path('hazard-update/<int:pk>/', HazardUpdate.as_view(), name='hazard-update'),
    path('hazard-delete/<int:pk>/', HazardDelete.as_view(), name='hazard-delete'),
]
