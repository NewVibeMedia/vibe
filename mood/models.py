from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Mood(models.Model):
    # has own table in db
    MOODS = (
        ("Very Negative", '0'),
        ("Negative", '1'),
        ("Neutral", '2'),
        ("Positive", '3'),
        ("Very Positive", '4'),
    )
    mood = models.CharField(max_length=50, choices=MOODS)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mood-detail', kwargs={'pk': self.pk})