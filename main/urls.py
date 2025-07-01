from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('cart/', views.cart, name="cart"),
    path('search/', views.cart, name="search-page"),
    path('checkout/', views.checkout, name="checkout-page"),
    path('error/', views.error, name="errorpage"),
    path('addproducts', views.addproducts, name="addproducts"),
    path('viewproducts', views.viewproducts, name="viewproducts"),
    
]