from django.urls import path

from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views

from . import views

from django.urls import reverse_lazy

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
    CategoryDelete,
    RiskList,
    RiskUpdate,
    RiskCreate,
    RiskDelete,
    StatusList,
    StatusUpdate,
    StatusCreate,
    StatusDelete,
    PasswordsChangeView,
    PasswordChangeSuccess
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='hazards'), name='logout'),
    path('register/', Register.as_view(), name='register'),

    path('', HazardList.as_view(), name='hazards'),
    path('hazard/<int:pk>/', HazardDetail.as_view(), name='hazard'),
    path('hazard/create/', HazardCreate.as_view(), name='hazard-create'),
    path('hazard/update/<int:pk>/', HazardUpdate.as_view(),
         name='hazard-update'),
    path('hazard/delete/<int:pk>/', HazardDelete.as_view(),
         name='hazard-delete'),

    path('profile/', profileView, name='profile-view'),
    path('profile/update', profileEdit, name='profile-update'),
    path('password/', PasswordsChangeView.as_view(), name='password-view'),
    path('password/update', PasswordChangeSuccess.as_view(),
         name='password-update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='hazard/components/password/password_reset.html'),
        name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='hazard/components/password/password_reset_done.html'),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='hazard/components/password/password_reset_confirm.html'),
        name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='hazard/components/password/password_reset_complete.html'),
        name="password_reset_complete"),
    path('categories', CategoryList.as_view(), name='categories'),
    path('categories/create/', CategoryCreate.as_view(), name='categories-create'),
    path('categories/update/<int:pk>/',
         CategoryUpdate.as_view(), name='categories-update'),
    path('categories/delete/<int:pk>/',
         CategoryDelete.as_view(), name='categories-delete'),

    path('risks', RiskList.as_view(), name='risks'),
    path('risks/create/', RiskCreate.as_view(), name='risks-create'),
    path('risks/update/<int:pk>/', RiskUpdate.as_view(), name='risks-update'),
    path('risks/delete/<int:pk>/', RiskDelete.as_view(), name='risks-delete'),

    path('statuses', StatusList.as_view(), name='statuses'),
    path('statuses/create/', StatusCreate.as_view(), name='statuses-create'),
    path('statuses/update/<int:pk>/',
         StatusUpdate.as_view(), name='statuses-update'),
    path('statuses/delete/<int:pk>/',
         StatusDelete.as_view(), name='statuses-delete'),
]
