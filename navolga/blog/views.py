from django.shortcuts import render ,get_object_or_404
from .models import Post,Category, Tag


def blog_home(request):

    return render(request,'blog/blog-home.html')

def blog_home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    return render(request, 'blog/blog-home.html', {'posts': posts})

# Individual post detail
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})

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