from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("category", views.display_category, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchlist/<int:id>", views.remove_watchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.add_watchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.add_comment, name="addComment"),
    path("bid/<int:id>", views.add_bid, name="addBid"),
    path("closeAuction/<int:id>", views.close_auction, name="closeAuction"),
]
