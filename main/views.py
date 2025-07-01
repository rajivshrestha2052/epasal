from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products, Product_Category, Order, Seller
from customer_login_sys.models import Customer
from .forms import  order_form
from customer_login_sys.forms import add_product, Customer_login


# Create your views here.

# view for frontpage
def frontpage(request):
    
    
    if request.method == 'POST':
        product = request.POST.get('cart-product')
        cart = request.session.get('cart')
        if cart:
            
            qty = cart.get(product)
            if qty:
                
                cart[product] = qty + 1
                
            else:
                cart[product] = 1
                
        else:
            cart ={}
            cart[product] = 1

        search_product = request.POST.get('search-product')
        print(search_product)
        if search_product:
            show_product = Products.search_product(search_product)
            print("search-product", show_product)
            
            return render (request,'main/search.html',{'products':show_product , 'search_word':search_product,})
            
            
        else:
            request.session['cart'] = cart
        
          
             
        return redirect('frontpage')

    elif request.method == 'GET':
        cat = Product_Category.objects.all()
   
        category = request.GET.get('category')
        
        if category:
            
            product = Products.get_product_cat(category)
            fcardcontainertitle = Products.get_cat_name(category)
        else:
            product = Products.get_all_products()
            fcardcontainertitle = "ALL PRODUCTS"
        
        if 'loginuser_email' in request.session:
            email = request.session.get('loginuser_email')
            logedin = Customer.get_customername_by_email(email)
        else:
            logedin = False
        
        cart = request.session.get('cart')
        if cart:
            product_qty = cart.values()
            carttot = 0
            for i in product_qty:
                carttot = carttot + i
        else:
            carttot = 0
        data={
            'products':product,
            'cat':cat,
            'fcardcontainertitle':fcardcontainertitle,
            'logedin':logedin,
            'carttot':carttot

        }
        return render(request, 'main/frontpage.html',data)
    

def cart(request):

    if request.method == 'POST':
        
        product = request.POST.get('cart-product')
        remove = request.POST.get('remove')
        del_prod = request.POST.get('del')
        cart = request.session.get('cart')
        if cart:
            
            qty = cart.get(product)
            if qty:
                if remove:
                    if qty<=1:
                        cart.pop(product)
                    else:
                        cart[product] = qty -1
                elif del_prod:
                        cart.pop(product)

                
                else:
                    cart[product] = qty + 1
                
            request.session['cart'] = cart
            
            return redirect('cart')

    else:

        if 'cart' in request.session:
            cart_session = request.session['cart']
            product_ids = list(cart_session.keys())
            cart_product = Products.get_product_by_id(product_ids)
            if 'loginuser_email' in request.session:
                email = request.session.get('loginuser_email')
                logedin = Customer.get_customername_by_email(email)
            else:
                logedin = False

            product_qty = request.session.get('cart').values()
            if product_qty:
                carttot = 0
                for i in product_qty:
                    carttot = carttot + i
            else:
                carttot = 0
            checkoutform = order_form()
            cart = {
                'products' : cart_product,
                'logedin' : logedin,
                'carttot': carttot,
                'checkoutform':checkoutform,
            }
                

                
                
            
            return render(request, 'customer_login_sys/cart.html',cart)

        else:
            if 'loginuser_email' in request.session:
                email = request.session.get('loginuser_email')
                logedin = Customer.get_customername_by_email(email)
            else:
                logedin = False
           
            return render(request,'customer_login_sys/cart.html', {'logedin':logedin})



def checkout(request):
    if request.method == 'POST':
        form = order_form(request.POST)
        if form.is_valid():

            if 'loginuser_id' in request.session:
                c_id = request.session['loginuser_id']
                cart = request.session.get('cart')
                logedin = Customer.objects.get(id=c_id)
                for keys, values in cart.items():
                    product = Products.get_product_price_by_id(keys)
                    print("==============",product.price)
                    neworder = Order()
                    neworder.customer_id = logedin
                    neworder.product_id = Products.objects.get(id=keys)
                    neworder.price = product.price
                    neworder.order_date = date.today()
                    neworder.quantity = values
                    neworder.shipping_address = form.cleaned_data['shipping_address']
                    neworder.save()
                del request.session['cart']

                return render(request, 'customer_login_sys/checkout.html',{'logedin': logedin})
            else:
                form = Customer_login()
                return render(request, "customer_login_sys/login.html", {'form':form})

        return HttpResponse("Success")
    else:
        return render(request, 'customer_login_sys/error.html' )


def error(request):
    return render(request, 'main/error.html')



def addproducts(request):
    if request.method == "POST":
        form = add_product(request.POST, request.FILES)
        email = request.session.get('loginseller_email')
        print(email)
        if form.is_valid():
            try:
                newproduct = Products()
                newproduct.product_name = form.cleaned_data['product_name']
                newproduct.seller_name = Seller.get_seller_by_email(email)
                newproduct.product_category = form.cleaned_data['product_category']
                newproduct.price = form.cleaned_data['price']
                newproduct.image = form.cleaned_data['image']
                newproduct.register_product()
                msg ="Successfully added new Product"
                
            except:
                msg ="error"

            data = {
                'logedin':email,
                'msg':msg,
            }
            return redirect("sellerprofile")
        else:
            return HttpResponse("Error")
        

    else:
        form = add_product()
        logedin = request.session.get('loginseller_email')
        return render(request, 'main/addproducts.html',{'form':form, 'logedin':logedin})


def viewproducts(request):
    if 'loginseller_email' in request.session:
        if request.method == "POST":
            return HttpResponse("hello")

        else:
            email = request.session.get('loginseller_email')
            
            try:
                seller = Seller.get_seller_by_email(email)
                
                products = Products.get_product_by_seller(seller)
                
            except:
                products = []
            return render(request, "main/viewproducts.html", {'products':products, 'logedin':email})



    else:
        return render(request,"main/error.html")

