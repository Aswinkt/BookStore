from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Author, Book, RequestLog

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'full_name', 'is_author')
    list_filter = ('is_author', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__email', 'user__full_name')
    list_filter = ('created_date', 'modified_date')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'published_date')
    list_filter = ('author', 'published_date', 'created_date')
    search_fields = ('title', 'description', 'author__user__email')
    date_hierarchy = 'published_date'

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'user', 'created_date')
    list_filter = ('method', 'created_date')
    search_fields = ('path', 'user__email')
    readonly_fields = ('method', 'path', 'user', 'created_date', 'modified_date')
