from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist-modification/<int:listing_id>", views.watchlist_modification, name="watchlist-modification"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("user-listings/<int:user_id>", views.user_listings, name="user_display"),
    path("my_bids", views.my_bids, name="my_bids"),
    path("categories", views.categories, name="categories"),
    path("active-category-listings/<str:category>", views.active_category_listings, name="active_category_listings")
]
