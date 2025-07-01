from django.contrib import admin
from .models import Customer
# Register your models here.

class CustomerView(admin.ModelAdmin):
    list_display =('email','l_name','f_name')


admin.site.register(Customer, CustomerView)

