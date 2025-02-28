from django.contrib import admin
from .models import CustomerDetail, Product, Cart, Order

# Register your models here.

@admin.register(CustomerDetail)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'address', 'city', 'state', 'pincode']
    search_fields = ['user__username', 'name', 'city', 'state']
    list_filter = ['state', 'city']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'short_description', 'original_price', 'discounted_price']
    search_fields = ['name', 'category']
    list_filter = ['category']
    ordering = ['name']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    search_fields = ['user__username', 'product__name']
    list_filter = ['user']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'formatted_total_price', 'order_at', 'status']
    search_fields = ['user__username', 'customer__name', 'product__name']
    list_filter = ['status', 'order_at']
    readonly_fields = ['order_at']

    def formatted_total_price(self, obj):
        return f"₹{obj.total_price:.2f}"  # Format price with currency symbol
    formatted_total_price.short_description = "Total Price"  # Rename column header
