from django.contrib import messages
from django.shortcuts import render
from .models import Basket, Category,Product, Slide,BasketItem
from django.shortcuts import render,get_object_or_404 , redirect


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


def basket_view(request):
    basket = Basket.objects.filter(user=request.user).select_related('user').first()
    items = basket.items.all() if basket else []
    total_items = sum(item.quantity for item in items)

    context = {
        "basket": basket,
        "total_items": total_items,
        "items": items,
        "total": basket.get_total() if basket else 0,
    }
    return render(request, "navolga_main/basket.html", context)

def categoryProducts(request,category_id):

    category = get_object_or_404(Category, id=category_id)
    category_products = category.products.all()
    categories = Category.objects.prefetch_related('products').all()
    basket = None
    items = []
    total_items = 0
    total = 0

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related('user').first()
        items = basket.items.all() if basket else []
        total_items = sum(item.quantity for item in items)
        total = basket.get_total() if basket else 0



    return render(request,'navolga_main/category_products.html',{
        'category': category,
        'category_products': category_products,
        'categories': categories,
        "basket": basket,
        "items": items,
        "total_items": total_items,
        "total": total,
    })


def product_detail(request,product_id):
    product = get_object_or_404(Product,id =product_id)
    related_products = Product.objects.filter(category = product.category)

    categories = Category.objects.prefetch_related('products').all()
    basket = None
    items = []
    total_items = 0
    total = 0

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related('user').first()
        items = basket.items.all() if basket else []
        total_items = sum(item.quantity for item in items)
        total = basket.get_total() if basket else 0


    return render(request, 'navolga_main/product_details.html',
                   {'product': product,
                    'related_products':related_products,
                    'categories': categories,
                    "basket": basket,
                    "items": items,
                    "total_items": total_items,
                    "total": total, })


def add_to_basket(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get("quantity", 1))

    # Check if the item is already in the basket
    basket_item, item_created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product
    )

    if not item_created:
        # If item already exists, increase the quantity
        basket_item.quantity += quantity
    else:
        # Set the quantity to the specified amount
        basket_item.quantity = quantity

    basket_item.save()

    messages.success(request, f"{product.name} has been added to your basket.")
    return redirect("home")  # Redirect to your product page