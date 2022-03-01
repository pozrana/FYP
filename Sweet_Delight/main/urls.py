from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('login.html', views.login),
    path('booking.html', views.booking)
]