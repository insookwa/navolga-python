from django.contrib import admin
from user.admin import admin_site
from .models import Category, Tag, Post, PostPhoto,Comment

class PostPhotoInline(admin.TabularInline):
    model = PostPhoto
    extra = 1
    fields = ['photo', 'is_featured']  # Use 'photo', not 'image'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostPhotoInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at')
    search_fields = ('author_name', 'content')

admin_site.register(Post)
admin_site.register(Category)
admin_site.register(Tag)
admin_site.register(Comment)