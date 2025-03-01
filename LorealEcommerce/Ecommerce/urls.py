from django.urls import path
from . import views

#------ To include Media file ---------------
from django.conf import settings
from django.conf.urls.static import static
#-----------------------------------------------

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Product Categories
    path('shampoo_categories/', views.shampoo_categories, name='shampoo_categories'),
    path('serum_categories/', views.serum_categories, name='serum_categories'),
    path('hair_colour_categories/', views.hair_colour_categories, name='hair_colour_categories'),
    
    # Product Details
    path('product_details/<int:id>/', views.product_details, name='product_details'),

    # Authentication & User Profile
    path('registration/', views.register, name='registration'),
    path('login/', views.log_in, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.log_out, name="logout"),
    path('changepassword/', views.changepassword, name="changepassword"),
]

#--------- This will add files to media folder -----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
