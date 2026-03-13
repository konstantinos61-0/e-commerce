from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError

from django.http import HttpResponseRedirect, Http404, HttpResponseNotAllowed, HttpResponseBadRequest

from django.shortcuts import render

from django.urls import reverse

from .models import Listing, Bid, Comment, User
from .forms import PartialListingForm, PartialBidForm, PartialCommentForm


def index(request):
    """Renders the homepage containing a list of all currently active listings"""
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(active=True).order_by("-created_at")
    })


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
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
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
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    """Render the listing creation form (GET) / Handle form submission (POST)"""

    # POST
    if request.method == "POST":
        listing = Listing(seller=request.user) # Prefill model instance with required fields excluded from the form.
        form = PartialListingForm(request.POST, instance=listing)

        if form.is_valid():
            listing = form.save() 
            return HttpResponseRedirect(reverse("listing", args=[listing.pk]))
    # GET
    else:
        form = PartialListingForm()

    # At this point, form is either empty or filled with data to be corrected.
    return render(request, "auctions/create_listing.html",{
        "form": form
    })


def listing(request, listing_id):
    """Render a specific listing in detail (also handle bid / comment submissions)"""
    context = {}

    user = request.user 

    # Update context with non-user-related data
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist") # Message for debugging purposes
    comments = listing.comments.all().order_by("-created_at")
    context.update({"comments": comments, "listing": listing})
    
    # Authenticated users can also bid, comment and see extra listing info
    if user.is_authenticated:
        # POST / GET control flow 
        if request.method == "POST" and request.POST.get("action") == "Place Bid":
            comment_form = PartialCommentForm()

            bid = Bid(listing=listing, bidder=user) # Prefill model instance with required fields excluded from the form.
            bid_form = PartialBidForm(request.POST, instance=bid)

            if bid_form.is_valid():
                bid = bid_form.save()
                listing.top_bid = bid.price
                listing.save() 
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        elif request.method == "POST" and request.POST.get("action") == "Post Comment":
            bid_form = PartialBidForm()
            
            comment = Comment(listing=listing, commenter=user) # Prefill model instance with required fields excluded from the form.
            comment_form = PartialCommentForm(request.POST, instance=comment)

            if comment_form.is_valid():
                comment_form.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
        elif request.method == "POST": # Handle invalid submission action
            return HttpResponseBadRequest(
                "<h2>400<h2/> <p>Something went wrong with the form submission. " \
                "Please go back to the listing's page and resubmit one of the available forms</p>")
    
        else: # GET case
            comment_form = PartialCommentForm()
            bid_form = PartialBidForm() 
    

        bids_made = len(listing.bids.all())   

        try:
            user.listings_watched.get(pk=listing_id)
            is_watched = True
        except Listing.DoesNotExist:
            is_watched = False

        is_top_bidder = False
        try:
            top_bid = listing.bids.all().get(price=listing.top_bid)
            if user == top_bid.bidder:
                is_top_bidder = True
        except Bid.DoesNotExist:
            pass
        
        # Add context for authenticated users
        context.update({
            "is_watched": is_watched,
            "is_top_bidder": is_top_bidder,
            "bids_made": bids_made,
            "bid_form": bid_form,
            "comment_form": comment_form
        })

    return render(request,"auctions/listing.html", context)


@login_required
def watchlist_modification(request, listing_id):
    """Add/Remove listing from current logged in user's watchlist"""

    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist") # Message for debugging purposes

    # Prevent watchlist-modification via GET method. Only POST method allowed to modify system state
    if request.method == "POST":
        listing.modify_watchlist(request.user) # Raises PermissionDenied if modify fails
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def watchlist(request):
    """Render a list of all listings that the current logged-in user have in their watchlist"""
    listings = request.user.listings_watched.all() 
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "watch": True
    })


@login_required
def close(request, listing_id):
    """Allow the currently logged in user to close the auction on one of their listings"""
    if request.method == "POST":
        user = request.user
        # TRY to get listing
        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing doesn't exist")

        listing.close(user) # Raises PermissionDenied if close fails
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    return HttpResponseNotAllowed(["POST"]) # Forbid GET method



@login_required
def user_listings(request, user_id):
    """Render a user page with a list of their listings"""
    seller = User.objects.get(pk=user_id)
    listings = Listing.objects.filter(seller=seller).order_by("-created_at")
    return render(request, "auctions/active_inactive.html", {
        "listings": listings,
        "seller": seller
    })


@login_required
def my_bids(request):
    """Render a user page with a list of all the listings they have bid on"""
    listings_bid_on = request.user.listings_bid_on.all()

    # Create a list of the user's listings that they have bid on (no duplicates for multiple bids)
    listings = []
    for listing in listings_bid_on:
        if listing not in listings:
            listings.append(listing) 
    return render(request, "auctions/active_inactive.html", {
        "listings": listings
    })



def categories(request):
    """Render a list of all the available listing categories to choose from"""

    # Use copy method on CATEGORIES dict so that the original object in memory stays intact. 
    # This way, Listing.CATEGORIES is reusable.
    categories = Listing.CATEGORIES.copy()
    categories.pop("")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def active_category_listings(request,category):
    """Render all active listings in the selected category"""

    categories = Listing.CATEGORIES.copy()
    categories.pop("")

    active_listings = Listing.objects.filter(category=category, active=True).order_by("-created_at")

    # Retrieve human_readable_category + Validate category URL parameter
    category_human_readable = categories.get(category)
    if not category_human_readable:
        raise Http404("Category not found")

    return render(request, "auctions/index.html", {
        "category": category,
        "category_human_readable": category_human_readable,
        "listings": active_listings
    })
    

