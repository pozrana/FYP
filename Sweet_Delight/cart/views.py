
from dataclasses import dataclass
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from main.models import FoodMenu


def cart(request):

	if request.user.is_authenticated:
		# accessing customer
		customer = request.user.customer
		#get the customer order or create it
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		#get the items attached to that orders
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart/cart.html', context)


def checkout(request):
	if request.user.is_authenticated:
		# accessing customer
		customer = request.user.customer
		#get the customer order or create it
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		#get the items attached to that orders
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	
	return render(request, 'cart/checkout.html', context)

def updateItem(request):
	# loads()- used to parse a valid JSON string and convert it into a Python Dictionary
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:',action)
	print('ProductId:',productId)

	# getting logged in customer
	customer = request.user.customer
	product = FoodMenu.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	#changing cutomer order and orer items
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	# timestamp gives long character field
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# accessing the total and set to float field
		total = float(data['form']['total'])
		order.transcation_id = transaction_id

		# check total passed in frontend is same as cart total
		if total == order.get_cart_total:
			order.complete = True
		order.save()

		# shipping logic
		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],

			)
	else:
		print('User is not logged in..')

	# print('data:', request.body)
	return JsonResponse('Payment Complete!', safe=False)

