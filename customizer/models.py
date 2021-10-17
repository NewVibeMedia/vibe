from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customizer(models.Model):

    FONT_CHOICES = (
        ("Roboto", "Roboto"),
        ("Oswald", "Oswald"),
        ("Patrick Hand", "Patrick Hand"),
        ("Yanone Kaffeesatz", "Yanone Kaffeesatz"),
        ("Crimson Text", "Crimson Text"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme_nav = models.CharField(max_length=7, default='#9FD19F')
    theme_background = models.CharField(max_length=7, default='#E8EBE8')
    font_size = models.IntegerField(default=12)
    font_style = models.CharField(max_length=128, choices=FONT_CHOICES, default="Roboto")

    @staticmethod
    def get_default_nav_color():
        return "#9FD19F"

    @staticmethod
    def get_default_bg_color():
        return "#E8EBE8"

    @staticmethod
    def get_default_font_size():
        return 16

    @staticmethod
    def get_default_font_style():
        return "Roboto"
