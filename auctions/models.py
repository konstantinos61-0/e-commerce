from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator

from django.core.exceptions import ValidationError, PermissionDenied

from django.utils.translation import gettext_lazy as _

### Important things i learned:
### 1) Keep business logic in one place (here, the model. see django doc topics/model). Why?
###    Cause when you import a model you also import all the business logic at once
###    Plus it makes the use of the model more clean in your views.

### 2) DRY design philosophy: don't repeat yourself!

### 3) Seperation of tasks. Templates, Views, Models, Forms (or ModelForms in this case), ...

### 4) 1 of the main Forms' class purpose is to validate the data!
### 5) Include docstrings in functions
### 6) Comments should explain the "why" not the "what" and give context when necessary
### 7) Write human readable code to reduce the need for comments that clutter code.


class User(AbstractUser):
    pass

class Listing(models.Model):

    CATEGORIES = {
        "": "Choose a Category",
        "SRTS": "Sports", 
        "TS": "Toys",
        "MU": "Music",
        "TCH": "Technology",
        "CLT": "Clothes",
        "HM": "Home",
        "O": "Other"
    } 

    # Required fields, Manually assigned
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.01)])
    category = models.CharField(max_length=100, choices=CATEGORIES)

    # Required fields, Automatically assigned
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    # Non required fields

    image_url = models.URLField(blank=True)

    # Editable = False for 2 reasons
    # 1) Don't want to display it on any modelforms, including django admin interface
    # 2) When set, the value has already been validated by the same standards by the Bid model.
    top_bid = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True, editable=False, validators=[MinValueValidator(0.01)])
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 

    # M2M Relationships

    # listings <-> users for bids
    bidders = models.ManyToManyField(User, through="Bid", related_name="listings_bid_on")

    # listings <-> users for comments
    commenters = models.ManyToManyField(User, through="Comment", related_name="listings_commented_on")

    # listings <-> userls for watch status
    watchers = models.ManyToManyField(User, through="Watching", related_name="listings_watched")


    def __str__(self):
        return f"{self.title}: {self.description}"
    
    # Validation useful for Django Admin Interface / a general defense against abnormal validation errors 
    def clean(self):
        if self.seller == self.winner:
            raise ValidationError("The listing owner can't be the winner of the auction")
        if self.top_bid:
            if self.top_bid < self.starting_bid:
                raise ValidationError("The top bid must be greater or equal to the starting bid")
    

    def modify_watchlist(self, user):
        """Add/Remove listing from currently logged-in user's watchlist."""

        # Prevent seller from adding listing to watchlist
        watching = Watching(watcher=user, listing=self)
        try:
            watching.full_clean()
        except ValidationError as e:
            raise PermissionDenied(e.args[0])

        listings_watched = user.listings_watched.all()
        if self not in listings_watched:
            Watching.objects.create(watcher=user, listing=self)
        else:
            Watching.objects.get(watcher=user, listing=self).delete()


    def close(self, user):
        """Close the listing by updating its active attribute"""
        if user == self.seller:
            if not self.top_bid:
                self.active = False
                self.save()
            else:
                self.active = False
                self.winner = self.bids.get(price=self.top_bid).bidder # Pick winner
                self.save()
        else:
            raise PermissionDenied("Closing a listing you don't own is not allowed.")

    

# Through table for M2M relationship listings <--> bidders (users)
class Bid(models.Model):
    
    # Relationship ForeignKeys
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    # Bid Description Fields
    price = models.DecimalField(decimal_places=2, max_digits=11, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.price} on {self.listing.title}"


    def clean(self):
        """Custom clean method. Checks for valid bids and raises ValidationError on failed attempts to bid"""
        # This check is necessary because the price might have not survived the form validation.
        if self.price:
            if not self.listing.top_bid and self.price < self.listing.starting_bid:
                raise ValidationError(
                    {"price": _("Bid must be greater or equal to starting bid")}
                )

            elif self.listing.top_bid and self.price <= self.listing.top_bid:
                raise ValidationError(
                    {"price": _("Bid must be greater than the current price")}
                )

        if self.listing.seller == self.bidder:
            raise ValidationError(
                {"bidder": _("You can't bid on a listing of your own")}
            )
        
        if self.listing.active == False:
            raise ValidationError(
                {"listing": _("You can't bid on a closed listing")}
            ) 
            


# Through table for M2M relationship between listing <--> commenters (users)
class Comment(models.Model):

    # Relationship ForeignKeys
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    # Comment Description Fields
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing.title} ({self.created_at})"
    
# Through table for M2M relationship between listing <--> users for watch status 
class Watching(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.listing.title} owned by {self.listing.seller} is in {self.watcher}'s Watchlist"

    def clean(self):
        if self.listing.seller == self.watcher:
            raise ValidationError("Adding a listing you own to your watchlist is not allowed.")

