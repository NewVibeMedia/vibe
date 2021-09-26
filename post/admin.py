from .models import Post
from django.contrib import admin

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'date_posted', 'author')
    list_filter = ('date_posted',)
    search_fields = ['title', ' content']

admin.site.register(Post, PostAdmin)