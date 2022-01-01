from django.contrib import admin
from . models import FoodMenu

# re

# Register the model in the admin section to manage
#admin object has attribute called site which is itself
#a object and this object has method called register
#we call this method and passing models class as a argument

admin.site.register(FoodMenu)
