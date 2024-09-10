from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
