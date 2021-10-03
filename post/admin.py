from .models import Post, UserPostOptions
from django.contrib import admin

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'date_posted', 'author')
    list_filter = ('date_posted',)
    search_fields = ['title', ' content']

class UserPostOptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'option_type', 'date_created')
    list_filter = ('option_type',)


admin.site.register(Post, PostAdmin)
admin.site.register(UserPostOptions, UserPostOptionAdmin)
