from django.urls import path
from . import views

app_name = 'photo_gallery'

urlpatterns = [
    path('', views.home, name='home'),
]