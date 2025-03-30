from django.contrib import admin
from django.urls import path,include
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Existing URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Add this new URL pattern
    path('products/', views.product_list, name='product-list'),
    
    # Updated Categories for Shoes
    path('men_categories/', views.men_categories, name='mencategories'),
    path('women_categories/', views.women_categories, name='womencategories'),
    path('kids_categories/', views.kids_categories, name='kidscategories'),
    
    # Updated Pet Details to Shoe Details
    path('shoe_details/<int:id>/', views.shoe_details, name='shoedetails'),
    
    # Authentication URLs
    path('registration/', views.registration, name='registration'),
    path('login/', views.log_in, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.log_out, name="logout"),
    path('changepassword/', views.changepassword, name="changepassword"),
    
    # Cart Functionality
    path('add_to_cart/<int:id>/', views.add_to_cart, name="addtocart"),
    path('view_cart/', views.view_cart, name="viewcart"),
    path('add_quantity/<int:id>/', views.add_quantity, name="add_quantity"),
    path('delete_quantity/<int:id>/', views.delete_quantity, name="delete_quantity"),
    path('delete_cart/<int:id>/', views.delete_cart, name="deletecart"),
    
    # Address Functionality
    path('address/', views.address, name='address'),
    path('delete_address/<int:id>/', views.delete_address, name='deleteaddress'),
    
    # Checkout and Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/<int:selected_address_id>/', views.payment_success, name='paymentsuccess'),
    path('payment_failed/', views.payment_failed, name='paymentfailed'),
    path('payment/', views.payment, name='payment'),
    
    # Order History
    path('orders/', views.orders_list, name='orders'),  # Add this new URL
    path('order-tracking/<int:order_id>/', views.order_tracking, name='order'),
    
    # Buy Now Functionality
    path('buynow/<int:id>/', views.buynow, name='buynow'),
    path('buynow_payment/<int:id>/', views.buynow_payment, name='buynowpayment'),
    path('buynow_payment_success/<int:selected_address_id>/<int:id>/', views.buynow_payment_success, name='buynowpaymentsuccess'),
    
    # Forgot Password
    path('forgotpassword/', views.forgot_password, name="forgotpassword"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
