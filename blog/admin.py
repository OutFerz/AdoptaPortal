from django.contrib import admin
from .models import Post, Category, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "slug")              
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)                     
    prepopulated_fields = {"slug": ("name",)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("name", "email", "body", "approved", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "content", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")  
    filter_horizontal = ("tags",)