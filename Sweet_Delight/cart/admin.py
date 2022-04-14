from django.contrib import admin

from .models import *


admin.site.register(Admin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)


