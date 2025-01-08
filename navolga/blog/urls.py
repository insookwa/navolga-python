from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.blog_home, name='home'),  # Blog homepage
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # Individual post
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),  # Posts by category
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),  # Posts by tag
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
