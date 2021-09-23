from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    # has own table in db
    POST_TYPES = (
        ("Gratitude", 'Gratitude'),
        ("Question", 'Question'),
        ("Personal", 'Personal'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField() 
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default=POST_TYPES[2])
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
          return reverse('post-detail', kwargs={'pk': self.pk})
    