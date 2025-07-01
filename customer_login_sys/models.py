from django.db import models
from django.db.models.fields import EmailField

# Create your models here.


class Customer(models.Model):
    f_name = models.CharField(max_length=100, verbose_name='First Name')
    m_name = models.CharField(max_length=100, blank=True)
    l_name = models.CharField(max_length=100, verbose_name='Last Name')
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=500, blank=True, default=email)
    password = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
    

    @staticmethod

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

    def get_customername_by_email(email):
        try:
            fname =  Customer.objects.get(email = email)
            return fname.f_name
        except:
            return False


    def register_user(self):
        self.save()


      



    






    