from django.shortcuts import render, redirect, get_object_or_404
from .models import Shoes, Cart, CustomerDetail, Order  # Make sure Cart model exists in models.py
from .forms import RegistrationForm, AuthenticateForm, ChangePasswordForm, UserProfileForm, AdminProfileForm, CustomerForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from datetime import datetime, timedelta
import random


# =============== For Paypal =========================
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
# =========================================================

# ================ Forgot Password ======================
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse


# Create your views here.
def home(request):
    cart_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    shoe = Shoes.objects.all()  # Added this line to define 'shoe' variable
    context = {
        'cart_count': cart_count,
        'shoe': shoe,
    }
    return render(request, 'core/home.html', context)



def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def men_categories(request):
    shoe = Shoes.objects.filter(category='MEN')
    return render(request, 'core/men_categories.html', {'shoe': shoe})


def women_categories(request):
    shoe = Shoes.objects.filter(category='WOMEN')
    return render(request, 'core/women_categories.html', {'shoe': shoe})


def kids_categories(request):
    shoe = Shoes.objects.filter(category='KIDS')
    return render(request, 'core/kids_categories.html', {'shoe': shoe})



def shoe_details(request, id):
    shoe = get_object_or_404(Shoes, id=id)
    return render(request, 'core/shoe_details.html', {'shoe': shoe})


# =======================================================================================


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                messages.success(request, 'Registration Successful !!')
                email = request.POST['email']
                user = User.objects.filter(email=email).first()
                if user:
                    send_mail(
                        'Registration Successful',
                        f'Thank you for choosing us!!',
                        'krishpytho1389@gmail.com',  # Use a verified email address
                        fail_silently=False,
                    )
                return redirect('registration')
        else:
            mf = RegistrationForm()
        return render(request, 'core/registration.html', {'mf': mf})
    else:
        return redirect('profile')


def log_in(request):
    if not request.user.is_authenticated:  # check whether user is not login, if so it will show login option
        if request.method == 'POST':  # otherwise it will redirect to the profile page
            mf = AuthenticateForm(request, request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request, 'core/login.html', {'mf': mf})
    else:
        return redirect('profile')


def profile(request):
    if request.user.is_authenticated:  # This checks whether user is login, if not it will redirect to login page
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST, instance=request.user)
            else:
                mf = UserProfileForm(request.POST, instance=request.user)
            if mf.is_valid():
                mf.save()
                messages.success(request, 'Profile Updated Successfully !!')
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request, 'core/profile.html', {'name': request.user, 'mf': mf})
    else:  # request.user returns the username
        return redirect('login')


def log_out(request):
    logout(request)
    return redirect('home')


def changepassword(request):  # Password Change Form
    if request.user.is_authenticated:  # Include old password
        if request.method == 'POST':
            mf = ChangePasswordForm(request.user, request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request, mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request, 'core/changepassword.html', {'mf': mf})
    else:
        return redirect('login')


# ============================ Add To Cart ====================================

def add_to_cart(request, id):
    if request.user.is_authenticated:
        shoe = Shoes.objects.get(pk=id)
        user = request.user
        Cart(user=user, product=shoe).save()
        messages.success(request, 'Added to cart successfully!')
        return redirect('shoedetails', id)
    else:
        return redirect('login')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, 'core/view_cart.html', {'cart_items': cart_items, })
    else:
        return redirect('login')


def add_quantity(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart, pk=id)
        product.quantity += 1
        product.save()
        return redirect('viewcart')
    else:
        return redirect('login')


def delete_quantity(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Cart, pk=id)
        if product.quantity > 1:
            product.quantity -= 1
            product.save()
        return redirect('viewcart')
    else:
        return redirect('login')


def delete_cart(request, id):
    shoe_cart = Cart.objects.get(pk=id)
    shoe_cart.delete()
    return redirect('viewcart')


# ================================ Address Page =========================
def address(request):
    if request.method == 'POST':
        mf = CustomerForm(request.POST)
        if mf.is_valid():
            user = request.user  # user variable store the current user i.e steveroger
            name = mf.cleaned_data['name']
            address = mf.cleaned_data['address']
            city = mf.cleaned_data['city']
            state = mf.cleaned_data['state']
            pincode = mf.cleaned_data['pincode']
            CustomerDetail(user=user, name=name, address=address, city=city, state=state, pincode=pincode).save()
            return redirect('address')
    else:
        mf = CustomerForm()
        address = CustomerDetail.objects.filter(user=request.user)
    return render(request, 'core/address.html', {'mf': mf, 'address': address})


def delete_address(request, id):
    if request.method == 'POST':
        de = CustomerDetail.objects.get(pk=id)
        de.delete()
    return redirect('address')


# ============================== Checkout Page ==============================

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    total =0
    delhivery_charge =100
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    final_price= delhivery_charge + total
    
    address = CustomerDetail.objects.filter(user=request.user)

    return render(request, 'core/checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'address':address})

# ============================== payment Page ==============================


def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        if not selected_address_id:
            messages.error(request, 'Please select a delivery address')
            return redirect('checkout')
        
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('viewcart')
        
        total = 0
        delivery_charge = 100
        for item in cart_items:
            item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
            total += item.product.price_and_quantity_total
        final_price = delivery_charge + total

        final_price_usd = "{:.2f}".format(float(final_price) / 82.0)

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': final_price_usd,
            'item_name': 'Cart Payment',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('paymentsuccess', kwargs={'selected_address_id': selected_address_id})),
            'cancel_return': request.build_absolute_uri(reverse('paymentfailed')),
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'core/payment.html', {
            'paypal': paypal_payment,
            'final_price': final_price,
            'final_price_usd': final_price_usd,
            'selected_address_id': selected_address_id,
            'cart_items': cart_items,
        })
    
    return redirect('checkout')


#
  

# ==================== Payment Success Page =====================================
def payment_success(request, selected_address_id):
    user = request.user
    address_data = CustomerDetail.objects.get(pk=selected_address_id)
    cart = Cart.objects.filter(user=request.user)
    for cart in cart:
        Order(user=user, customer=address_data, quantity=cart.quantity, shoe=cart.product).save()
        cart.delete()

    send_mail(
        'Order successfully Placed',
        f'Your Order is Booking Sucessfully',
        'krishpytho1389@gmail.com',  # Use a verified email address
        [request.user.email],
        fail_silently=False,
    )
    return render(request, 'core/payment_success.html')


# ==================== Payment Failed Page =====================================

def payment_failed(request):
    return render(request, 'core/payment_failed.html')


# ========================= Order Page ==================================

def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Calculate expected arrival date (e.g., 7 days from now)
    expected_arrival_date = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    
    # Generate a random tracking number
    tracking_number = f"USPS{random.randint(100000000000, 999999999999)}"
    
    context = {
        'order': order,
        'expected_arrival_date': expected_arrival_date,
        'tracking_number': tracking_number,
    }
    return render(request, 'core/order.html', context)
# ========================================== Buy Now ========================================================

def buynow(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    shoe = Shoes.objects.get(pk=id)
    delivery_charge = 100
    final_price = delivery_charge + shoe.discounted_price
    
    # Set default quantity for buy now
    shoe.quantity = 1
    # Calculate total for single item
    shoe.total = shoe.discounted_price * shoe.quantity
    
    address = CustomerDetail.objects.filter(user=request.user)
    if not address.exists():
        messages.warning(request, 'Please add a delivery address first')
        return redirect('address')

    return render(request, 'core/buynow.html', {
        'final_price': final_price,
        'address': address,
        'shoe': shoe,
        'delivery_charge': delivery_charge
    })


def buynow_payment(request,id):

    if request.method == 'POST':
        selected_address_id = request.POST.get('buynow_selected_address')

    Shoe = Shoes.objects.get(pk=id)     # cart_items will fetch product of current user, and show product available in the cart of the current user.
    delhivery_charge =100
    final_price= delhivery_charge + Shoe.discounted_price
    
    address = CustomerDetail.objects.filter(user=request.user)
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Shoes',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================

    return render(request, 'core/payment.html', {'final_price':final_price,'address':address,'Shoe':Shoe,'paypal':paypal_payment})




def buynow_payment_success(request, selected_address_id, id):
    user = request.user
    customer_data = CustomerDetail.objects.get(pk=selected_address_id)
    shoe = Shoes.objects.get(pk=id)
    
    Order(user=user, customer=customer_data, shoe=shoe, quantity=1).save()

    send_mail(
        'Order successfully Placed',
        f'Your Order is Booking Sucessfully',
        'krishpytho1389@gmail.com',  # Use a verified email address
        [request.user.email],
        fail_silently=False,
    )
    
    return render(request, 'core/buynow_payment_success.html', {'shoe': shoe})


# ================================== Forget Password ====================================================

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'krishpytho1389@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request, 'please enter valid email address')
    return render(request, 'core/forgot_password.html')

    # return render(request,'core/forgot_password.html',)


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')


def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'core/product_list.html', {'products': products})



def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_at')  # Changed from created_at to order_at
    return render(request, 'core/orders.html', {'orders': orders})


def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'core/wishlist.html', {'wishlist_items': wishlist_items})


def add_to_wishlist(request, id):
    product = get_object_or_404(Shoes, id=id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, 'Added to wishlist!')
    return redirect('shoedetails', id=id)


def remove_from_wishlist(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id, user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Removed from wishlist!')
    return redirect('wishlist')