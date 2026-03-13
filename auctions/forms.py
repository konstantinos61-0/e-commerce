from django import forms

from .models import Listing, Comment, Bid

### Questions
### 1) In a ModelForm instance, where you supply missing model fields
###    through the instance keyword, does the call to ModelForm.is_valid()
###    first update the model instance before calling the Model.full_clean()
###    for that model instance (which ofc lives inside the ModelForm as the 
###    instance attribute)? 
###    A: Yes

class PartialListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        labels = {
            "title": "",
            "description": "",
            "starting_bid": "",
            "image_url": "",
            "category": ""
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Title",
                "class": "form-control"
            }),
            "description": forms.TextInput(attrs={
                "placeholder": "Description",
                "class": "form-control"
            }),
            "starting_bid": forms.NumberInput(attrs={
                "placeholder": "Starting Bid ($)",
                "class": "form-control"
            }),
            "image_url": forms.URLInput(attrs={
                "placeholder": "https://example.com",
                "class": "form-control"
            }),
            "category": forms.Select(
                attrs={
                "placeholder": "Category",
                "class": "form-control"
                }
            )
        }

class PartialCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": ""
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "Content",
                "class": "form-control",
                "rows": "3" 
            }),
        }

class PartialBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {
            "price": ""
        }
        widgets = {
            "price": forms.NumberInput(attrs={
                "placeholder": "Bid ($)",
                "class": "form-control"
            }),
        }