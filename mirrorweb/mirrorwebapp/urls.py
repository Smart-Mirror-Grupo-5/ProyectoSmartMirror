from django.urls import path
from mirrorwebapp import views

urlpatterns = [
    path('', views.index, name='index'),
]