from django.db import models
from msilib.schema import Property
from re import T
from turtle import back
from xml.sax.handler import property_declaration_handler
from django.db import models
from django.contrib.auth.models import User
from main.models import FoodMenu

# cascade - if one relations' item is deleted, another linked must be deleted
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


# cutomer can have many orders, complete - if complete is false, we need to continue add items on cart
# if it is True, we add items on different order
# set_null - if customer deleted, we do not need to delete order 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    # order shipping status
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False: 
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        #querry all child order items
        orderitems = self.orderitem_set.all()
        #add all order items in total
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        #querry all child order items
        orderitems = self.orderitem_set.all()
        #add all order items in cart
        total = sum([item.quantity for item in orderitems])
        return total

# items that are needed to add on our order with many to one relationship
# order is a cart and orderitem is the item within a cart
# cart can have multiple order items
class OrderItem(models.Model):
    product = models.ForeignKey(FoodMenu, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity 
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address





