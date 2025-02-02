
from django.contrib import admin
from django.urls import path,include
from user.admin import admin_site  # Import your custom admin site

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', admin_site.urls),  # Custom admin URL for both /admin/ and /admin/savings_admin/
    path('user/', include('user.urls')),
    path('shop/', include('navolga_main.urls')),
    path('', include('blog.urls')),
    path('speaking-club/', include('speaking_club.urls')),
    # path('payments/', include('payments.urls')),

]
