from django.contrib import admin
from user.admin import admin_site


from .models import Category,Product,Slide

admin_site.register(Category)
admin_site.register(Product)
admin_site.register(Slide)


admin.site.site_header = "navolga Admin Panel"  # Main header on the admin dashboard
admin.site.site_title = "Navolga Administration"  # Title in the browser tab
admin.site.index_title = "Welcome to Navolga Admin Panel"  # Subtitle on the admin dashboard
