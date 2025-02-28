from django.db import models
from django.contrib.auth.models import User
 # For generating SEO-friendly slugs


# Customer Details
class CustomerDetail(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'),
        ('BR', 'Bihar'), ('CT', 'Chhattisgarh'), ('GA', 'Goa'), ('GJ', 'Gujarat'),
        ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'), ('KL', 'Kerala'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'),
        ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'),
        ('OR', 'Odisha'), ('PB', 'Punjab'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'), ('TG', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'), ('JK', 'Jammu and Kashmir'), ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'), ('PY', 'Puducherry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    pincode = models.CharField(max_length=6)  # Changed to CharField for handling leading zeros

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"


# Product Model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('SHAMPOO', 'Shampoo'), ('HAIR_COLOR', 'Hair Color'), ('SERUM', 'Serum'),
        ('SKINCARE', 'Skincare'), ('MAKEUP', 'Makeup'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images')

    def get_final_price(self):
        """Returns the final discounted price."""
        return self.discounted_price

    def __str__(self):
        return f"{self.name} - ₹{self.get_final_price()}"


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        """Returns the total price for the product in the cart."""
        return self.product.get_final_price() * self.quantity

    def __str__(self):
        return f"Cart {self.id} - {self.product.name} (Qty: {self.quantity})"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'), ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    @property
    def total_price(self):
        """Calculate total price automatically."""
        return self.product.get_final_price() * self.quantity

    def __str__(self):
        return f"Order {self.id} - {self.product.name} (Qty: {self.quantity})"
