from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import (
    HazardList,
    HazardDetail,
    HazardCreate,
    HazardUpdate,
    HazardDelete,
    CustomLoginView,
    Register,
    profileView,
    profileEdit,
    CategoryList,
    CategoryUpdate,
    CategoryCreate,
    CategoryDelete
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='hazards'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('', HazardList.as_view(), name='hazards'),
    path('hazard/<int:pk>/', HazardDetail.as_view(), name='hazard'),
    path('hazard-create/', HazardCreate.as_view(), name='hazard-create'),
    path('hazard-update/<int:pk>/', HazardUpdate.as_view(), name='hazard-update'),
    path('hazard-delete/<int:pk>/', HazardDelete.as_view(), name='hazard-delete'),
    path('profile/', profileView, name='profile-view'),
    path('profile/edit', profileEdit, name='profile-edit'),
    path('categories', CategoryList.as_view(), name='categories'),    
    path('categories-create/', CategoryCreate.as_view(), name='categories-create'),
    path('categories-update/<int:pk>/', CategoryUpdate.as_view(), name='categories-update'),
    path('categories-delete/<int:pk>/', CategoryDelete.as_view(), name='categories-delete'),
]
