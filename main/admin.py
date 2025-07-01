from django.contrib import admin
from .models import Seller, Product_Category, Products, Order


# Register your models here.

class Products_View(admin.ModelAdmin):
    list_display =('product_name','seller_name','image_tag','product_category','price')

admin.site.register(Seller)
admin.site.register(Product_Category)
admin.site.register(Products, Products_View)
admin.site.register(Order)
