from django.urls import path

from .views import *


urlpatterns = [
	path("add-to-cart-<int:food_id>/", AddToCartView.as_view(), name="addtocart"),
	path("my-cart/", MyCartView.as_view(), name="mycart"),
	path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
	path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

	path("checkout/", CheckoutView.as_view(), name="checkout"),

	path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
	path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),

	path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
	path("login/", CustomerLoginView.as_view(), name="customerlogin"),
	path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),

	path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
	path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),

	path("search/", SearchView.as_view(), name="search"),

	path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
	path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
	path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),
         name="adminorderdetail"),
	path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
	path("admin-order-<int:pk>-change/",
         AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),


]