# e-commerce
### Description
A django web application for an eBay-like e-commerce auction site. It allows users to post auction listings, place bids on listings, comment and add listings to a "watchlist". I completed this project as part of HarvardX's CS50-W course for web programming with python and JavaScript. 

### Specification
The implementation of my auction site adheres to the following specifications:
- **Create Listing**: Users are be able to visit a page to create a new listing. They are required to specify the listing title, text-based description, starting bid and category. Optionally, they can provide a URL for an image.
- **Active Listings Page**: The default website route displays all of the currently active auction listings. For each listing the page exhibits the title, description, current price and photo (if applicable)
- **Listing page**: Clicking on a listing takes the user to a page specific to that listing where all the details about it are displayed, including its current price. If the user is signed in, they can also:
  - Add/Remove the item to/from their "watchlist"
  - Bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
  - Close the listing, if they are the listing's owner. This makes the highest bidder win rendering the listing inactive.
  - See if they have won the auction on a closed listing.
  - Add comments to the listing page. All comments made on a listing must be displayed.
- **Watchlist**: Every signed in user can visit a page that includes all the listings they have added to their watchlist. Clicking on any of them takes the user to that listing's page.
- **Categories**: Users can visit a page that displays all of the categories. Clicking on the name of any category any takes the user to a page that displays all active listings of that category.
- **User listings**: Users can visit a page where they can can see a list of their listings.
- **User Bids**: Users can visit a page where they can can see a list of all of the listings they have bid on.
- **Django admin interface**: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.
- **Models**: My application implements the following Model Classes that handle storing data: Listing, Bid, Comment, Watching.
- **ModelForms**: My application also includes the following ModelForm classes that handle form generation: PartialListingForm, PartialCommentForm, PartialBidForm.

### What I implemented
This application's distribution code is available at: https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip (accessed 12 March 2026). It includes only the following routes: login, logout and register as well as a basic html layout for the navigation bar, the login form and the registration form. I studied and understood them and then moved on to implement the rest of the app. Specifically, I implemented the following:
- Routes (views): index, create_listing, listing, watchlist_modification, watchlist, close, user_listings, my_bids, categories, active_category_listings
- Models: the entirety of the Models.
- ModelForms: the entirety of the ModelForms.
- HTML templates: I substantially extended the HTML templates for all the views as well as for some http error codes, utilizing the appropriate semantic HTML elements
- CSS styles: I implemented the entirety of the styles.css file (except a single rule) which is included in every template. The styles add a basic feel while promoting visual clarity. Responsive design using flex-box and relative sizing.
