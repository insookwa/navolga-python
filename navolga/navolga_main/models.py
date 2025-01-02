from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)


    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    dosage_form = models.CharField(max_length=100, blank=True, null=True)  # e.g., tablet, syrup
    strength = models.CharField(max_length=50, blank=True, null=True)  # e.g., 500mg
    prescription_required = models.BooleanField(default=False)  # Indicates if prescription is needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=255,null=True,blank=True)
    ingredient = models.CharField(max_length=255,null=True,blank=True)
    age_suitable = models.CharField(max_length=255,null=True,blank=True)
    size = models.CharField(max_length=255,null=True,blank=True)
    side_effects = models.CharField(max_length=255,null=True,blank=True)
    generic = models.CharField(max_length=255,null=True,blank=True)
    works_by= models.CharField(max_length=255,null=True,blank=True)
    manufacturer = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='static/img/product_images/', blank=True, null=True) 

    def __str__(self):
        return self.name
    
class Slide(models.Model):
    title = models.CharField(max_length=200, help_text="The headline for the slide")
    background_image = models.ImageField(upload_to='slides/backgrounds/', blank=True, null=True)
    description = models.TextField(help_text="Detailed description or subtitle for the slide")
    background_color = models.CharField(
        max_length=7, 
        default="#FFFFFF", 
        help_text="Background color in HEX (e.g., #FFFFFF for white)"
    )
    image = models.ImageField(upload_to='static/img/slides_images/', help_text="Image displayed on the slide")
    alt_text = models.CharField(
        max_length=200, 
        default="Slide image", 
        help_text="Description of the image for accessibility"
    )
    app_store_url = models.URLField(
        blank=True, 
        help_text="Link to the app on the App Store"
    )
    google_play_url = models.URLField(
        blank=True, 
        help_text="Link to the app on Google Play"
    )
    is_active = models.BooleanField(default=True, help_text="Toggle to show or hide this slide")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basket")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket of {self.user.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())