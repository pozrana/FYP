from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('booking/', views.booking),
    path('dashboard/booking/', views.booking),
    path('dashboard/', views.dashboard),
    path('dashboard/cart/', views.cart),

    # path('contact/', views.contact),
    # path('gallery/', views.gallery),
    # path('menu/', views.menu),
    # path('opening/', views.opening),
    # path('services/', views.services),
    # path('about/', views.about),
    # path('home/', views.home)
]