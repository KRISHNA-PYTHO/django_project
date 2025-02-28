from django.urls import path
from . import views

# To include media files in development mode
from django.conf import settings
from django.conf.urls.static import static

app_name = 'your_app_name'  # Change to your actual Django app name

urlpatterns = [
    # Basic Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.changepassword, name='change_password'),

    # Products
    path('products/', views.loreal_products, name='products'),
#    path('products/<int:id>/', views.loreal_details, name='product_details'),

    # Shopping Cart & Orders
#   path('cart/', views.loreal_cart, name='cart'),
    
    # Categories
    path('categories/shampoo/', views.shampoo_categories, name='shampoo_categories'),
    path('categories/serum/', views.serum_categories, name='serum_categories'),
    path('categories/hair-color/', views.hair_colour_categories, name='hair_colour_categories'),
]

# Media files serving in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



