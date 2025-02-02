from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='shop_home'),
    path('product/<int:product_id>/',views.product_detail,name='product_details'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name="add_to_basket"),
    path('basket/', views.basket_view, name="basket"),
    # path('basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('about/', views.aboutUs, name='about_us'),
    path('category/<int:category_id>/', views.categoryProducts, name='category_products'),
    path('contact/', views.contactUs, name='contact_us'),
    # path('ipn/', views.payment_callback, name='payment_callback'),
    # path('search/', views.search_products, name='search_products'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)