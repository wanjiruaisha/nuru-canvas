from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)

from django.urls import path, reverse_lazy
from .forms import LoginForm, StyledPasswordChangeForm

from . import views
from .forms import LoginForm

app_name = 'photo_gallery'

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register'
    ),
    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path('', views.home, name='home'),
    path(
        'photos/<int:pk>/',
        views.photo_detail,
        name='photo_detail'
    ),
    path(
    'photos/<int:pk>/react/<str:reaction_type>/',
    views.react_to_photo,
    name='react_to_photo'
    ),
    path(
    'profile/',
    views.profile,
    name='profile'
    ),
    path(
    'profile/edit/',
    views.edit_profile,
    name='edit_profile'
    ),
    path(
    'profile/password-change/',
    PasswordChangeView.as_view(
        template_name='photo_gallery/password_change.html',
        form_class=StyledPasswordChangeForm,
        success_url=reverse_lazy(
            'photo_gallery:password_change_done'
        )
    ),
    name='password_change'
    ),
    path(
    'profile/password-change/done/',
    PasswordChangeDoneView.as_view(
        template_name='photo_gallery/password_change_done.html'
    ),
    name='password_change_done'
    ),
    

]