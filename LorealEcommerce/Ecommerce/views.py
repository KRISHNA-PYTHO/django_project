from django.shortcuts import render
from . models import Pet
# Create your views here.
def home(request):
    return render(request, 'ecommerce/home.html')


def about(request):
    return render(request, 'ecommerce/about.html')


def contact(request):
    return render(request, 'ecommerce/contact.html')


def dog_categories(request):
    dc = Pet.objects.filter(category='DOG')
    return render(request,'ecommerce/dog_categories.html',{'dc':dc})


def cat_categories(request):
    dc = Pet.objects.filter(category='CAT')
    return render(request,'ecommerce/cat_categories.html',{'dc':dc})


def bird_categories(request):
    return render(request,'ecommerce/bird_categories.html')

def pet_details(request,id):
    dc= Pet.objects.get(pk=id)
    return render(request,'ecommerce/pet_details.html',{'dc':dc})
