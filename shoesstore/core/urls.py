from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
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
    
    
    # Payment URLs
    # Buy Now URLs
    path('buynow/<int:id>/', views.buynow, name='buynow'),
    path('buynow-payment/<int:id>/', views.buynow_payment, name='buynowpayment'),
    path('buynow-payment-success/<int:selected_address_id>/<int:id>/', views.buynow_payment_success, name='buynowpaymentsuccess'),
    
    # Regular Payment URLs
    path('payment/', views.payment, name='payment'),
    path('payment-success/<int:selected_address_id>/', views.payment_success, name='paymentsuccess'),
    path('payment-failed/', views.payment_failed, name='paymentfailed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)