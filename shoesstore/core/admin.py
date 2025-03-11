from django.contrib import admin
from .models import CustomerDetail,Shoes,Cart,Order
# Register your models here.

@admin.register(CustomerDetail)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']


@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'colour', 'size', 'original_price', 'discounted_price', 'discount_percentage')
    list_filter = ('category', 'colour', 'size')
    search_fields = ('name', 'category')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','shoe','quantity','order_at','status',]