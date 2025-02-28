from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import RegistrationForm, AuthenticateForm, ChangePasswordForm, UserProfileForm, AdminProfileForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

# Home Page
def home(request):
    return render(request, 'ecommerce/home.html')

# About Page
def about(request):
    return render(request, 'ecommerce/about.html')

# Contact Page
def contact(request):
    return render(request, 'ecommerce/contact.html')

# Category Views
def shampoo_categories(request):
    shampoos = Product.objects.filter(category='SHAMPOO')
    return render(request, 'ecommerce/shampoo_categories.html', {'products': shampoos})

def serum_categories(request):
    serums = Product.objects.filter(category='SERUM')
    return render(request, 'ecommerce/serum_categories.html', {'products': serums})

def hair_colour_categories(request):
    hair_colours = Product.objects.filter(category='HAIR_COLOR')  # Fixed category name
    return render(request, 'ecommerce/hair_colour_categories.html', {'products': hair_colours})

# Product Details
def loreal_products(request, id):
    product = get_object_or_404(Product, pk=id)  # Safer than Product.objects.get()
    return render(request, 'ecommerce/product_details.html', {'product': product})

# User Registration
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successful! Please log in.')
            return redirect('login')  # Redirect to login instead of 'registration'
    else:
        form = RegistrationForm()
    
    return render(request, 'ecommerce/register.html', {'form': form})

# User Login
def log_in(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticateForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    
    form = AuthenticateForm()
    return render(request, 'ecommerce/login.html', {'form': form})

# User Profile
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=request.user) if request.user.is_superuser else UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully!')
    else:
        form = AdminProfileForm(instance=request.user) if request.user.is_superuser else UserProfileForm(instance=request.user)
    
    return render(request, 'ecommerce/profile.html', {'name': request.user, 'form': form})

# User Logout
def log_out(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# Change Password
def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'ecommerce/changepassword.html', {'form': form})
