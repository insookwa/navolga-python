from django.contrib import admin
from .models import Category, Tag, Post, PostPhoto

class PostPhotoInline(admin.TabularInline):
    model = PostPhoto
    extra = 5  # Display 5 extra empty fields for new photos
    fields = ('image', 'caption', 'is_featured')
    readonly_fields = ('is_featured',)  # Optional: Prevent changing `is_featured` inline

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'tags', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostPhotoInline]


from django.contrib import admin
from .models import Category, Tag, Post, Comment

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