from django.shortcuts import render
from .models import Category,Product, Slide
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



def home(request):
    slides = Slide.objects.filter(is_active=True).order_by("created_at")

    categories = Category.objects.prefetch_related('products').all()
    products = Product.objects.all()


    # categories = Category.objects.prefetch_related('products').all()
    # basket = Basket.objects.filter(user=request.user).select_related('user').first()
    # items = basket.items.all() if basket else []
    # total_items = sum(item.quantity for item in items)


    return render(request, 'navolga_main/index.html',{
        'products':products,
        'categories': categories,
        "slides": slides
        })


def aboutUs(request):
    categories = Category.objects.all()
    return render(request, 'navolga_main/about.html',{
        'categories':categories,

    })


def contactUs(request):


    categories = Category.objects.all()

    return render(request,'navolga_main/contact_us.html',{
        'categories':categories,

    })


