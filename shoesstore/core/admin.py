from django.contrib import admin
from .models import Shoes, CustomerDetail, Cart, Order

class ShoesAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'original_price', 'discounted_price', 'colour', 'size']
    list_filter = ['category', 'colour', 'size']
    search_fields = ['name', 'category']

# Register your models only once
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(CustomerDetail)
admin.site.register(Cart)
admin.site.register(Order)