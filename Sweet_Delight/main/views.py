from django.shortcuts import render

from . models import FoodMenu

# Create your views here.
def index(request):
    menus = FoodMenu.objects.all()
    return render(request, 'index.html', {'menus': menus})

    

    
