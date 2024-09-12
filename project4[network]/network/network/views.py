import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import User, Post, Follow, Like


def unlike(request, post_id):
    _post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    _like = Like.objects.filter(user=user, post=_post)
    _like.delete()
    return JsonResponse({"message": "Like removed!"})


def like(request, post_id):
    _post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    new_like = Like(user=user, post=_post)
    new_like.save()
    return JsonResponse({"message": "Like added!"})


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})
    return None # Should not get here


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    # Get posts the logged in user has liked
    all_likes = Like.objects.all()
    users_likes = []
    for _like in all_likes:
        if _like.user.id == request.user.id:
            users_likes.append(_like.post.id)

    # Get like count for all posts
    post_likes_count = {}
    for _post in all_posts:
        likes_count = Like.objects.filter(post=_post).count()
        post_likes_count[_post.id] = likes_count

    return render(request, "network/index.html", {
        "allPosts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "whoYouLiked": users_likes,
        "post_likes": post_likes_count
    })


def post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        _post = Post(content=content, user=user)
        _post.save()
        return HttpResponseRedirect(reverse(index))
    return None # Should not get here


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    _following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    #try:
    check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
    is_following = bool(len(check_follow) != 0)

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    # Get posts the logged in user has liked
    all_likes = Like.objects.all()
    users_likes = []
    for _like in all_likes:
        if _like.user.id == request.user.id:
            users_likes.append(_like.post.id)

    # Get like count for all posts
    post_likes_count = {}
    for _post in all_posts:
        likes_count = Like.objects.filter(post=_post).count()
        post_likes_count[_post.id] = likes_count

    return render(request, "network/profile.html", {
        "allPosts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        "following": _following,
        "followers": followers,
        "isFollowing": is_following,
        "user_profile": user,
        "whoYouLiked": users_likes,
        "post_likes": post_likes_count
    })


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_people = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()

    following_posts = []

    for _post in all_posts:
        for person in following_people:
            if person.user_follower == _post.user:
                following_posts.append(_post)

    # Pagination
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    # Get posts the logged in user has liked
    all_likes = Like.objects.all()
    users_likes = []
    for _like in all_likes:
        if _like.user.id == request.user.id:
            users_likes.append(_like.post.id)

    # Get like count for all posts
    post_likes_count = {}
    for _post in all_posts:
        likes_count = Like.objects.filter(post=_post).count()
        post_likes_count[_post.id] = likes_count

    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page,
        "whoYouLiked": users_likes,
        "post_likes": post_likes_count
    })


def follow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    _follow = Follow(user=current_user, user_follower=user_follow_data)
    _follow.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


def unfollow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    _follow = Follow.objects.get(user=current_user, user_follower=user_follow_data)
    _follow.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


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
        return render(request, "network/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/register.html")
