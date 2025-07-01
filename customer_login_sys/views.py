from django.db.models.base import Model
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer 
from .forms import Customer_login,Customer_Signup,Seller_Signup
from django.db import DatabaseError, IntegrityError
from django.contrib import messages
from main.models import Seller, Order

# Create your views here.


class User_login():
    def login_user(request):
        error_msg= None
        if request.method == 'POST':
            form = Customer_login(request.POST)
       
            if form.is_valid():
               
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                loginuser = Customer.get_customer_by_email(username)
                
                if loginuser:
                    if password == loginuser.password:
                        request.session['loginuser_id'] = loginuser.id
                        request.session['loginuser_email'] = loginuser.email
                        

                        return redirect('profile')


                    else:
                        error_msg = "Username and Password donot match"
                        return render(request, "customer_login_sys/login.html", {'form':form,'error_msg':error_msg})

                else:
                    error_msg = "Username and Password donot match"
                    return render(request, "customer_login_sys/login.html", {'form':form,'error_msg':error_msg})
                
        else:
            
            form = Customer_login()
        return render(request, "customer_login_sys/login.html", {'form':form})


    def logout_user(request):
        request.session.clear()
        return redirect('frontpage')



    def signup_user(request):
        error_msg= None
        if request.method == 'POST':
            form = Customer_Signup(request.POST)
            if form.is_valid():
                try:
                    newcustomer = Customer()
                    newcustomer.f_name = form.cleaned_data['f_name']
                    newcustomer.m_name = form.cleaned_data['m_name']
                    newcustomer.l_name = form.cleaned_data['l_name']
                    if form.cleaned_data['mobile'].isdigit() and len(form.cleaned_data['mobile']) == 10:
                        newcustomer.mobile = form.cleaned_data['mobile']
                    else:
                        error_msg = "Invalid Mobile Number"
                    newcustomer.address = form.cleaned_data['address']
                    if not Customer.objects.filter(email=form.cleaned_data['email']):
                        newcustomer.email = form.cleaned_data['email']
                        newcustomer.username = form.cleaned_data['email']
                   
                    else:
                        error_msg = "Email Address Already Exists"
                    newcustomer.password = form.cleaned_data['password']
                    newform = Customer_login()
                    if not error_msg:
                        newcustomer.register_user()
                        return render(request, "customer_login_sys/login.html",{'form':newform})
                    else:
                        return render(request, "customer_login_sys/signup.html",{'form':form,'error_msg':error_msg})
                    
                except:
                    error_msg = "oops Something went wrong in your registration"
                    return render(request, "customer_login_sys/signup.html",{'form':form, 'error_msg':error_msg})
                
        else:
            
            form = Customer_Signup()
        return render(request, "customer_login_sys/signup.html", {'form':form})



class CustomerProfile:
    def customer_profile(request):
        if 'loginuser_email' in request.session:
            email = request.session.get('loginuser_email')
            logedin = Customer.get_customername_by_email(email)
            
            try:
                product_qty = request.session.get('cart').values()
            except:
                product_qty = []
                
            # for showing total in order
            
            c_id = request.session['loginuser_id']
            
            getorder = Order()
            total = getorder.get_order_price_by_customer(c_id)
            
            # for showing total cart

            if product_qty:
                carttot = 0
                for i in product_qty:
                    carttot = carttot + i
            else:
                carttot = 0

            # for showing total in order
            order_total = 0
            if total:
                for i in total:
                    order_total = order_total + (float(i.price)*float(i.quantity))
            else:
                order_total = 0
            
            return render(request, "customer_login_sys/dashboard.html",{'logedin':logedin, 'carttot':carttot, 'ordertot': order_total, 'email':email})
        else:
            return redirect("errorpage")


    
    
    def customer_info(request):

        
        if 'loginuser_email' in request.session:
            email = request.session.get('loginuser_email')
            c_id = request.session['loginuser_id']
            logedin = Customer.get_customername_by_email(email)

            return render(request, "customer_login_sys/userinfo.html", {'logedin':logedin, 'cid':c_id,})
          
                    
            
        else:
            return redirect("errorpage")


    def changeuserpass(request):
        if 'loginuser_email' in request.session:
            if request.method == "POST":
                oldpass = request.POST.get('oldpass')
                newpass = request.POST.get('newpass')
                confirmpass = request.POST.get('confirmpass')
                email = request.session.get('loginuser_email')
                logedin = Customer.get_customername_by_email(email)
                user = Customer.get_customer_by_email(email)
                if oldpass == user.password:
                    if newpass == confirmpass:
                        user.password = newpass
                        user.save()
                        msg = "Password Changed Successfully"
                        return render(request, "customer_login_sys/dashboard.html", {'msg':msg, 'logedin':logedin,})
                    else:
                        msg = "Passwords donot match"
                        return render(request, "customer_login_sys/changepass.html", {'msg':msg, 'logedin':logedin,})
                else:
                    msg = "Incorrect Password"
                    return render(request, "customer_login_sys/changepass.html", {'msg':msg, 'logedin':logedin,})

            else:
                email = request.session.get('loginuser_email')
                logedin = Customer.get_customername_by_email(email)
                return render(request, "customer_login_sys/changepass.html", {'logedin':logedin,})

        else:
            return redirect("errorpage")
                


#
#
#    for seller part
#
#
#

class Seller_login():
    def login_seller(request):
        error_msg= None
        if request.method == 'POST':
            form = Customer_login(request.POST)
       
            if form.is_valid():
               
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                loginseller = Seller.get_seller_by_email(username)
                
                if loginseller:
                    if password == loginseller.password:
                        request.session['loginseller_id'] = loginseller.id
                        request.session['loginseller_email'] = loginseller.email
                        

                        return redirect('sellerprofile')


                    else:
                        error_msg = "Username and Password donot match"
                        return render(request, "customer_login_sys/loginseller.html", {'form':form,'error_msg':error_msg})

                else:
                    error_msg = "Username and Password donot match"
                    return render(request, "customer_login_sys/loginseller.html", {'form':form,'error_msg':error_msg})
                
        else:
            
            form = Customer_login()
        return render(request, "customer_login_sys/loginseller.html", {'form':form})


    def logout_seller(request):
        request.session.clear()
        return redirect('frontpage')



    def signup_seller(request):
        error_msg= None
        if request.method == 'POST':
            form = Seller_Signup(request.POST)
            if form.is_valid():
                try:
                    newcustomer = Seller()
                    newcustomer.seller_name = form.cleaned_data['seller_name']
                    if form.cleaned_data['mobile'].isdigit() and len(form.cleaned_data['mobile']) == 9:
                        newcustomer.pan_no = form.cleaned_data['pan_no']
                    else:
                        error_msg = "Invalid PAN Number"
                    
                    if form.cleaned_data['mobile'].isdigit() and len(form.cleaned_data['mobile']) == 10:
                        newcustomer.mobile = form.cleaned_data['mobile']
                    else:
                        error_msg = "Invalid Mobile Number"
                    newcustomer.address = form.cleaned_data['address']
                    if not Seller.objects.filter(email=form.cleaned_data['email']):
                        newcustomer.email = form.cleaned_data['email']
                        
                   
                    else:
                        error_msg = "Email Address Already Exists"
                    newcustomer.password = form.cleaned_data['password']
                    newform = Customer_login()
                    if not error_msg:
                        newcustomer.register_seller()
                        return render(request, "customer_login_sys/loginseller.html",{'form':newform})
                    else:
                        return render(request, "customer_login_sys/signupseller.html",{'form':form,'error_msg':error_msg})
                    
                except:
                    error_msg = "oops Something went wrong in your registration"
                    return render(request, "customer_login_sys/signup.html",{'form':form, 'error_msg':error_msg})
                
        else:
            
            form = Seller_Signup()
        return render(request, "customer_login_sys/signup.html", {'form':form})



class SellerProfile:
    def seller_profile(request):
        if 'loginseller_email' in request.session:
            email = request.session.get('loginseller_email')
            logedin = Seller.get_sellername_by_email(email)
            
            try:
                product_qty = request.session.get('cart').values()
            except:
                product_qty = []
                
            # for showing total in order
            
            c_id = request.session['loginseller_id']
            
            getorder = Order()
            total = getorder.get_order_price_by_customer(c_id)
            
            # for showing total cart

            if product_qty:
                carttot = 0
                for i in product_qty:
                    carttot = carttot + i
            else:
                carttot = 0

            # for showing total in order
            order_total = 0
            if total:
                for i in total:
                    order_total = order_total + (float(i.price)*float(i.quantity))
            else:
                order_total = 0
            
            return render(request, "customer_login_sys/dashboardseller.html",{'logedin':logedin, 'carttot':carttot, 'ordertot': order_total, 'email':email})
        else:
            return redirect("errorpage")


    
    
    def seller_info(request):

        
        if 'loginseller_email' in request.session:
            email = request.session.get('loginseller_email')
            c_id = request.session['loginseller_id']
            logedin = Seller.get_sellername_by_email(email)
            return render(request, "customer_login_sys/userinfo.html", {'logedin':logedin, 'cid':c_id,})
                    
            
        else:
            return redirect("errorpage")


    def changesellerpass(request):
        if 'loginseller_email' in request.session:
            if request.method == "POST":
                print("it runed")
                oldpass = request.POST.get('oldpass')
                newpass = request.POST.get('newpass')
                confirmpass = request.POST.get('confirmpass')
                email = request.session.get('loginseller_email')
                logedin = Seller.get_sellername_by_email(email)
                user = Seller.get_seller_by_email(email)
                if oldpass == user.password:
                    if newpass == confirmpass:
                        user.password = newpass
                        user.save()
                        msg = "Password Changed Successfully"
                        print("loged in ", logedin)
                        return redirect('sellerprofile')
                    else:
                        msg = "Passwords donot match"
                        return render(request, "customer_login_sys/changesellerpass.html", {'msg':msg, 'logedin':logedin,})
                else:
                    msg = "Incorrect Password"
                    return render(request, "customer_login_sys/changesellerpass.html", {'msg':msg, 'logedin':logedin,})

            else:
                email = request.session.get('loginseller_email')
                logedin = Seller.get_sellername_by_email(email)
                return render(request, "customer_login_sys/changesellerpass.html", {'logedin':logedin,})

        else:
            print("Ends hers")
            return redirect("errorpage")
                


            




            

