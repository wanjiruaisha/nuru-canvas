from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

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
]