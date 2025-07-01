from django.urls import path
from . import views

urlpatterns = [
    path('', views.User_login.login_user, name="loginpage"),
    path('signup', views.User_login.signup_user, name='signuppage'),
    path('logout', views.User_login.logout_user, name="logout"),
    path('profile', views.CustomerProfile.customer_profile, name="profile"),
    path('userinfo', views.CustomerProfile.customer_info, name="userinfo"),
    path('changepass', views.CustomerProfile.changeuserpass, name="changepass"),
    path('login-seller', views.Seller_login.login_seller, name="sellerloginpage"),
    path('sellersignup', views.Seller_login.login_seller, name='sellersignuppage'),
    path('sellerprofile', views.SellerProfile.seller_profile, name="sellerprofile"),
    path('changesellerpass', views.SellerProfile.changesellerpass, name="changesellerpass"),
]