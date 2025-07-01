from django import forms
from main.models import Products

class Customer_login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})

class Customer_Signup(forms.Form):
    
    f_name = forms.CharField(max_length=50, label ="First Name")
    m_name = forms.CharField(max_length=50, required=False, label ="Middle Name")
    l_name = forms.CharField(max_length=50, label ="Last Name")
    mobile = forms.CharField(max_length=10,label ="Mobile Number")
    address = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200, label ="Email Address")
    
    password = forms.CharField(max_length=100)
    f_name.widget.attrs.update({'class': 'form-control','placeholder':'First Name'})
    m_name.widget.attrs.update({'class': 'form-control','placeholder':'Middle Name'})
    l_name.widget.attrs.update({'class': 'form-control','placeholder':'Last Name'})
    mobile.widget.attrs.update({'class': 'form-control'})
    address.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control', 'placeholder':'example@123.com'})
    password.widget.attrs.update({'class': 'form-control'})


    #
    #
    # for seller
    #
    #
    #

class Seller_Signup(forms.Form):

    seller_name = forms.CharField(max_length=50, label ="First Name")
    pan_no = forms.CharField(max_length=9, required=False, label ="Middle Name")
    mobile = forms.CharField(max_length=10,label ="Mobile Number")
    address = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200, label ="Email Address")
    password = forms.CharField(max_length=100)
    
    seller_name.widget.attrs.update({'class': 'form-control','placeholder':'First Name'})
    pan_no.widget.attrs.update({'class': 'form-control','placeholder':'Last Name'})
    mobile.widget.attrs.update({'class': 'form-control'})
    address.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control', 'placeholder':'example@123.com'})
    password.widget.attrs.update({'class': 'form-control'})



class add_product(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name','product_category','price','image']
    
    
    # product_name = forms.CharField(max_length=100)
    # # product_category = forms.CharField(max_length=100)
    # price = forms.CharField(max_length=10)
    # image = forms.ImageField()
    
    # product_name.widget.attrs.update({'class': 'form-control'})
    # # product_category.widget.attrs.update({'class': 'form-control'})
    # price.widget.attrs.update({'class': 'form-control'})
    # image.widget.attrs.update({'class': 'form-control'})

    

        

        











    
