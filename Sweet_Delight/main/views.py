from django.shortcuts import render

from . models import FoodMenu, ImageGallery

# Create your views here.
def index(request):
    menus = FoodMenu.objects.all()
    galleries = ImageGallery.objects.all()
    return render(request, 'index.html', {'menus': menus, 'galleries': galleries})

def login(request):
    return render(request, 'login.html')    

    

    
