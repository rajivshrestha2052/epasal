import datetime
from statistics import mode
from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.html import mark_safe
from customer_login_sys.models import Customer

# Create your models here.
class Seller(models.Model):
    seller_name = models.CharField(max_length=100)
    pan_no = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)



    def __str__(self):
        return self.seller_name

    
    @staticmethod

    def get_seller_by_email(email):
        try:
            return Seller.objects.get(email = email)
        except:
            return False

    def get_sellername_by_email(email):
        try:
            fname =  Seller.objects.get(email = email)
            return fname
        except:
            return False


    def register_seller(self):
        self.save()


class Product_Category(models.Model):
    product_category= models.CharField(max_length=100)  


    def __str__(self) -> str:
        return self.product_category     


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    seller_name = models.ForeignKey('Seller', on_delete=models.CASCADE, blank=False, null=False)
    product_category =  models.ForeignKey('Product_Category', on_delete=models.CASCADE, blank=False, null=False)
    price = models.FloatField(max_length=8)
    image = models.ImageField(upload_to ='uploads')


    def __str__(self) -> str:
        return self.product_name

    def image_tag(self):
       
        return mark_safe('<img src="%s" width="150" height="150"/>'% (self.image.url))


    @staticmethod

    def get_all_products():
        return Products.objects.all()[::-1]


    def get_product_cat(category_id):
        if category_id:
            return Products.objects.filter(product_category=category_id)[::-1]
        else:
            return Products.objects.all()[::-1]

    def get_cat_name(category_id):
        return Product_Category.objects.get(id = category_id)


    def get_product_by_id(product_ids):
        return Products.objects.filter(id__in  = product_ids)

    def get_product_price_by_id(product_ids):
        return Products.objects.get(id = product_ids)

    def search_product(product_name):
        return Products.objects.filter(product_name__icontains = product_name)

    
    def get_product_by_seller(email):
        return Products.objects.filter(seller_name  = email)

    def register_product(self):
        self.save()


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete= models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete= models.SET_DEFAULT, default="")
    order_date = models.DateField()
    price = models.CharField(max_length=10)
    quantity = models.IntegerField()
    shipping_address = models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return str(self.order_date)


    @staticmethod

    def get_order_price_by_customer(id):
        return Order.objects.filter(customer_id = id)







