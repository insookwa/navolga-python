from django.shortcuts import render ,get_object_or_404
from .models import Post,Category, Tag,PostPhoto
from django.db.models import Prefetch


def blog_home(request):
    

    posts = Post.objects.filter(status='published').order_by('-created_at').prefetch_related(
        Prefetch('photos', queryset=PostPhoto.objects.all(), to_attr='post_photos')
    )

    # Prefetch only the featured photos
    featured_posts = posts[:3]
    featured_posts_with_photos = Post.objects.filter(id__in=[post.id for post in featured_posts]).prefetch_related(
        Prefetch('photos', queryset=PostPhoto.objects.filter(is_featured=True), to_attr='featured_photos')
    )

    # Debugging: Check featured photos
    for post in featured_posts_with_photos:
        if hasattr(post, 'featured_photos') and post.featured_photos:
            print(f"Featured image for {post.title}: {post.featured_photos[0].photo.url}")
        else:
            print(f"No featured image for {post.title}")

    return render(request, 'blog/blog-home.html', {
        'posts': posts,
        'featured_posts': featured_posts_with_photos,
    })

# Individual post detail
def post_detail(request, slug):

    other_posts = Post.objects.filter(status='published').order_by('-created_at').prefetch_related(

    Prefetch('photos', queryset=PostPhoto.objects.all(), to_attr='post_photos')
    )

    post = get_object_or_404(Post, slug=slug, status='published')

    
    posts = Post.objects.filter(status='published').order_by('-created_at').prefetch_related(
    Prefetch('photos', queryset=PostPhoto.objects.all(), to_attr='post_photos')
    )
    return render(request, 'blog/post_details.html', {'post': post ,'other_posts':other_posts})

# Posts by category
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

# Posts by tag
def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').order_by('-created_at')
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})