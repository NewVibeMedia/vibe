from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Mood(models.Model):
    # has own table in db
    MOODS = (
        ('0', "Very Negative"),
        ('1', "Negative"),
        ('2', "Neutral"),
        ('3', "Positive"),
        ('4', "Very Positive"),
    )
    mood = models.CharField(max_length=50, choices=MOODS)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['date_posted', 'author']]

    def __str__(self):
        return self.mood

    def get_absolute_url(self):
        return reverse('mood-detail', kwargs={'pk': self.pk})

    def chart_data(self):
        unix_time = self.date_posted.replace(tzinfo=timezone.utc).timestamp()
        return [unix_time, self.mood]