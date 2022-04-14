from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import requests


from .models import *
from .forms import *
from main.models import FoodMenu

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
class AddToCartView(EcomMixin,TemplateView):
	template_name = "cart/addtocart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# get product id from requested url
		product_id = self.kwargs['food_id']

		# get product
		product_obj = FoodMenu.objects.get(id=product_id)

		# check if cart exists
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			this_product_in_cart = cart_obj.cartproduct_set.filter(
				product=product_obj)
			
			# item already exists in cart
			if this_product_in_cart.exists():
				cartproduct = this_product_in_cart.last()
				cartproduct.quantity += 1
				cartproduct.subtotal += product_obj.price
				cartproduct.save()
				cart_obj.total += product_obj.price
				cart_obj.save()
			# new item is added in cart
			else:
				cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
				cart_obj.total += product_obj.price
				cart_obj.save()
		else:
			cart_obj = Cart.objects.create(total=0)
			self.request.session['cart_id'] = cart_obj.id
			cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
			cart_obj.total += product_obj.price
			cart_obj.save()
			
		return context

class MyCartView(EcomMixin, TemplateView):
	template_name = "cart/mycart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# to fetch cart
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
		else:
			cart = None
		
		context['cart'] = cart
		return context

class ManageCartView(EcomMixin, View):
	def get(self, request, *args, **kwargs):
		cp_id = self.kwargs['cp_id']
		action = request.GET.get("action")
		cp_obj = CartProduct.objects.get(id=cp_id)
		cart_obj = cp_obj.cart

		if action == "inc":
			cp_obj.quantity += 1
			cp_obj.subtotal += cp_obj.rate
			cp_obj.save()
			cart_obj.total += cp_obj.rate
			cart_obj.save()

		elif action == "dcr":
			cp_obj.quantity -= 1
			cp_obj.subtotal -= cp_obj.rate
			cp_obj.save()
			cart_obj.total -= cp_obj.rate
			cart_obj.save()
			if cp_obj.quantity == 0:
				cp_obj.delete()

		elif action == "rmv":
			cart_obj.total -= cp_obj.subtotal
			cart_obj.save()
			cp_obj.delete()
		else:
			pass

		return redirect("mycart")

class EmptyCartView(EcomMixin, View):
	def get(self, request, *args, **kwargs):
		cart_id = request.session.get("cart_id", None)
		if cart_id:
			cart = Cart.objects.get(id=cart_id)
			cart.cartproduct_set.all().delete()
			cart.total = 0
			cart.save()
		return redirect("mycart")	

class CheckoutView(EcomMixin, CreateView):
	template_name = "cart/checkout.html"
	form_class = CheckoutForm
	success_url = reverse_lazy("home")

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and request.user.customer:
			pass
		else:
			return redirect("/carts/login/?next=/carts/checkout/")
		return super().dispatch(request, *args, **kwargs)	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cart_id = self.request.session.get("cart_id", None)
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
		else:
			cart_obj = None

		context['cart'] = cart_obj

		return context
	
	def form_valid(self, form):
		cart_id = self.request.session.get("cart_id")
		if cart_id:
			cart_obj = Cart.objects.get(id=cart_id)
			form.instance.cart = cart_obj
			form.instance.subtotal = cart_obj.total
			form.instance.discount = 0
			form.instance.total = cart_obj.total
			form.instance.order_status = "Order Received"
			del self.request.session['cart_id']
			pm = form.cleaned_data.get("payment_method")
			order = form.save()
			if pm == "Khalti":
				return redirect(reverse("khaltirequest") + "?o_id=" + str(order.id))
			

		else:
			return redirect("home")
		return super().form_valid(form)

class KhaltiRequestView(View):
	def get(self, request, *args, **kwargs):
		o_id = request.GET.get("o_id")
		order = Order.objects.get(id=o_id)
		context = {
            "order": order
        }
		return render(request, "cart/khaltirequest.html", context)

class KhaltiVerifyView(View):
	def get(self, request, *args, **kwargs):
		token = request.GET.get("token")
		amount = request.GET.get("amount")
		o_id = request.GET.get("order_id")
		print(token, amount, o_id)
		
		url = "https://khalti.com/api/v2/payment/verify/"
		payload = {
            "token": token,
            "amount": amount
        }
		headers = {
            "Authorization": "Key test_secret_key_e870cfff05194c559c7e89cab66ad904"
        }
		
		order_obj = Order.objects.get(id=o_id)
		
		response = requests.post(url, payload, headers=headers)
		resp_dict = response.json()
		if resp_dict.get("idx"):
			success = True
			order_obj.payment_completed = True
			order_obj.save()
		else:
			success = False
		data = {
            "success": success
        }
		return JsonResponse(data)

class CustomerRegistrationView(CreateView):
	template_name = "register.html"
	form_class = CustomerRegistrationForm
	success_url = reverse_lazy("home")

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = User.objects.create_user(username, password)
		form.instance.user = user
		login(self.request, user)
		return super().form_valid(form)
	
	def get_success_url(self):
		if "next" in self.request.GET:
			next_url = self.request.GET.get("next")
			return next_url
		else:
			return self.success_url

class CustomerLogoutView(View):
	def get(self, request):
		logout(request)
		return redirect("home")

class CustomerLoginView(FormView):
	template_name = "login.html"
	form_class = CustomerLoginForm
	success_url = reverse_lazy("home")

	# form_valid method is a type of post method and is available in createview formview and updateview
	def form_valid(self, form):
		uname = form.cleaned_data.get("username")
		pword = form.cleaned_data.get("password")
		usr = authenticate(username=uname, password=pword)
		if usr is not None and Customer.objects.filter(user=usr).exists():
			login(self.request, usr)
		else:
			return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
		return super().form_valid(form)
	
	def get_success_url(self):
		if "next" in self.request.GET:
			next_url = self.request.GET.get("next")
			return next_url
		else:
			return self.success_url

class CustomerProfileView(TemplateView):
	template_name = "cart/customerprofile.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
			pass
		else:
			return redirect("/carts/login/?next=/carts/profile/")
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		customer = self.request.user.customer
		context['customer'] = customer
		orders = Order.objects.filter(cart__customer=customer).order_by("-id")
		context["orders"] = orders	
		return context

class CustomerOrderDetailView(DetailView):
	template_name = "cart/customer-order-detail.html"
	model = Order
	context_object_name = "ord_obj"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
			order_id = self.kwargs["pk"]
			order = Order.objects.get(id=order_id)
			if request.user.customer != order.cart.customer:
				return redirect("customerprofile")
			
		else:
			return redirect("/carts/login/?next=/carts/profile/")
		return super().dispatch(request, *args, **kwargs)

class SearchView(TemplateView):
	template_name = "cart/search.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		kw = self.request.GET.get("keyword")
		results = FoodMenu.objects.filter(
			Q(item_name__icontains=kw) | Q(desc__icontains=kw))
		print(results)
		context["results"] = results
		return context

# Admin Pages
class AdminLoginView(FormView):
	template_name = "adminpages/adminlogin.html"
	form_class = CustomerLoginForm
	success_url = reverse_lazy("adminhome")


	def form_valid(self, form):
		uname = form.cleaned_data.get("username")
		pword = form.cleaned_data.get("password")
		usr = authenticate(username=uname, password=pword)
		if usr is not None and Admin.objects.filter(user=usr).exists():
			login(self.request, usr)
		else:
			return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
		return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin,TemplateView):
	template_name = "adminpages/admin-home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["pendingorders"] = Order.objects.filter(order_status="Order Received").order_by("-id")
		return context

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
	template_name = "adminpages/admin-order-detail.html"
	model = Order
	context_object_name = "ord_obj"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["allstatus"] = ORDER_STATUS
		return context

class AdminOrderListView(AdminRequiredMixin, ListView):
	template_name = "adminpages/admin-order-list.html"
	queryset = Order.objects.all().order_by("-id")
	context_object_name = "allorders"

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		order_id = self.kwargs["pk"]
		order_obj = Order.objects.get(id=order_id)
		new_status = request.POST.get("status")
		order_obj.order_status = new_status
		order_obj.save()
		return redirect(reverse_lazy("adminorderdetail", kwargs={"pk": order_id}))


