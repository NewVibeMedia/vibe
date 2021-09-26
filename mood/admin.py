from .models import Mood
from django.contrib import admin

# Register your models here.
class MoodAdmin(admin.ModelAdmin):
    list_display = ('mood', 'date_posted', 'author')
    list_filter = ('date_posted',)
    search_fields = ['date_posted']

admin.site.register(Mood, MoodAdmin)
