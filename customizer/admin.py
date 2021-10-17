from .models import Customizer
from django.contrib import admin

# Register your models here.
class CustomizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_nav', 'theme_background', 'font_size', 'font_style')
    list_filter = ('user',)
    search_fields = ['user']

admin.site.register(Customizer, CustomizerAdmin)
