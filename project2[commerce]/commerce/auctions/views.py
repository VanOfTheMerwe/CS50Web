from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


# View to display a posted listing
def listing(request, id):
    _listing = Listing.objects.get(pk=id)
    in_watchlist = request.user in _listing.watchList.all()
    comments = Comment.objects.filter(listing=_listing)
    author = request.user.username == _listing.owner.username
    return render(request, "auctions/listing.html", {
        "listing": _listing,
        "isListingInWatchlist": in_watchlist,
        "allComments": comments,
        "isOwner": author
    })


# Close auction url
def close_auction(request, id):
    _listing = Listing.objects.get(pk=id)
    _listing.active = False
    _listing.save()
    seller = request.user.username == _listing.owner.username
    in_watchlist = request.user in _listing.watchList.all()
    comments = Comment.objects.filter(listing=_listing)
    return render(request, "auctions/listing.html", {
        "listing": _listing,
        "isListingInWatchlist": in_watchlist,
        "allComments": comments,
        "isOwner": seller,
        "update": True,
        "message": "This auction has been closed."
    })


# Handles creating new bids from user data
def add_bid(request, id):
    bid = request.POST['newBid']
    _listing = Listing.objects.get(pk=id)
    in_watchlist = request.user in _listing.watchList.all()
    comments = Comment.objects.filter(listing=_listing)
    author = request.user.username == _listing.owner.username

    # Check if a new bid was added to the listing
    if int(bid) > _listing.price.bid:
        new_bid = Bid(user=request.user, bid=int(bid))
        new_bid.save()
        _listing.price = new_bid
        _listing.save()
        return render(request, "auctions/listing.html", {
            "listing": _listing,
            "message": "Bid was updated successfully",
            "update": True,
            "isListingInWatchlist": in_watchlist,
            "allComments": comments,
            "isOwner": author,
        })
    return render(request, "auctions/listing.html", {
        "listing": _listing,
        "message": "Failed to update bid!",
        "update": False,
        "isListingInWatchlist": in_watchlist,
        "allComments": comments,
        "isOwner": author,
    })


# Handle creating comments from users
def add_comment(request, id):
    author = request.user
    _listing = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    comment = Comment(
        author = author,
        listing = _listing,
        message = message
    )

    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


# View to render a specific users watchlist
def watchlist(request):
    user = request.user
    listings = user.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


# Url to remove a listing from someones watchlist
def remove_watchlist(request, id):
    _listing = Listing.objects.get(pk=id)
    user = request.user
    _listing.watchList.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


# Url to add a listing to the users watchlist
def add_watchlist(request, id):
    _listing = Listing.objects.get(pk=id)
    user = request.user
    _listing.watchList.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


# Home page. Renders all active listings.
def index(request):
    listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories,
    })


# View to display listings in a specific category
def display_category(request):
    if request.method == "POST":
        form = request.POST['category']
        category = Category.objects.get(name=form)
        listings = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories,
        })
    return redirect(reverse("index"))


# View to allow users to create listings. Handles user listing
# post data too.
def create_listing(request):
    # Render page if accessed with GET
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories,
        })

    # Other get user post data
    title = request.POST['title']
    descript = request.POST['description']
    image = request.POST['image']
    price = request.POST['price']
    category_name = request.POST['category']
    user = request.user
    category = Category.objects.get(name=category_name)

    bid = Bid(bid=int(price), user=user)
    bid.save()

    # Create listing
    _listing = Listing(
        title=title,
        description=descript,
        image=image,
        price=bid,
        category=category,
        owner = user
    )
    _listing.save()

    # Redirect to listing
    return HttpResponseRedirect(reverse(index))


# View to allow users to login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "auctions/login.html")


# Url to logout signed in user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# User registration page and logic
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")
