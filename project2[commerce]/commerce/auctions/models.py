from django.contrib.auth.models import AbstractUser
from django.db import models


# Basic user model
class User(AbstractUser):
    pass


# Simple category name model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


# User bid model. Defines bid amount & user who placed the bid
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userBid')


# Action listing: defines data related to listings posted
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    watchList = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return str(self.title)


# User comments model. Defines comments posted by users on listings
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userComment')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listingComment')
    message = models.CharField(max_length=200)

    def __str__(self):
        return F"{self.author} comment on {self.listing}: {self.message}"
