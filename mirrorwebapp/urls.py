from django.urls import path
from mirrorwebapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
]