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

class UserPostOptions(models.Model):

    OPTION_TYPES = (
        ("Save", "Save"),
        ("Hide", "Hide"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option_type = models.CharField(max_length=4, choices=OPTION_TYPES, default=OPTION_TYPES[0])
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{str(self.user.username)} [{self.option_type}] {str(self.post)} on {str(self.date_created)}"

    @classmethod
    def create(cls, user, post, option_type):
        instance = cls(user=user, post=post, option_type=option_type)
        instance.save()

