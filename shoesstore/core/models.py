from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerDetail(models.Model):
     STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('JK', 'Jammu and Kashmir'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]

     user = models.ForeignKey(User, on_delete=models.CASCADE)  
     name = models.CharField(max_length=100)
     address = models.CharField(max_length=100)
     city = models.CharField(max_length=100)
     state = models.CharField(max_length=2, choices=STATE_CHOICES)
     pincode = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )
    
     def __str__(self):
        return str(self.id)
    
class Shoes(models.Model):
        CATEGORY_CHOICES = [
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('KIDS', 'Kids'),
    ]

        COLOUR_CHOICES = [
        ('RED', 'Red'),
        ('BLUE', 'Blue'),
        ('BLACK', 'Black'),
        ('WHITE', 'White'),
        ('GREEN', 'Green'),
        ('YELLOW', 'Yellow'),
    ]

        SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

        name = models.CharField(max_length=100)
        category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
        small_description = models.CharField(max_length=300)
        description = models.TextField()
        original_price = models.IntegerField()
        discounted_price = models.IntegerField()
        shoe_image = models.ImageField(upload_to='shoe_image/', null=True, blank=True)
        colour = models.CharField(max_length=20, choices=COLOUR_CHOICES, default='BLACK')
        size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='M')
        discount_percentage = models.IntegerField(default=0) 

        def __str__(self):
         return str(self.name)

        def save(self, *args, **kwargs):
        # Automatically calculate discount percentage
         if self.original_price and self.discounted_price:
            self.discount_percentage = int(((self.original_price - self.discounted_price) / self.original_price) * 100)
         super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"

    @property
    def price_and_quantity_total(self):
        return self.product.discounted_price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"