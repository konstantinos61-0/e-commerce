# commerce — Web Application
### Description
A Django web application for an eBay-like e-commerce auction site. It allows users to post auction listings, place bids on listings, comment on them and add them to a "watchlist". I completed this project as part of HarvardX's CS50-W course for Web Programming with Python and JavaScript. 

### Demo
A live demo video is available at: https://www.youtube.com/watch?v=au95n-cWGZ0&feature=youtu.be

### Installation
To run the project locally:
1. Make sure that Python is installed on your system.
2. Install the Django framework for Python.
3. Clone the repository.
4. From within the repository directory execute the following commands:
   - `python manage.py migrate` to synchronize the defined models with the database schema.
   - `python manage.py runserver` to run the local server.
  
### Tech Stack
- Back-end: Python (Django) 
- Front-end: HTML, (mostly) pure CSS, Bootstrap
- Database: SQLite

### Features
The website offers the following core features:
- **Authentication**: User authentication and authorization provided by the default Django Authentication System.
- **Create Listing**: Users are able to visit a page to create a new listing. They are required to specify the listing's title, a text-based description, the starting bid and a category. Optionally, they can provide a URL for an image.
- **Active Listings Page**: The default website route displays all of the currently active auction listings. For each listing the page displays the title, description, current price and photo (if applicable).
- **Listing page**: Clicking on a listing takes the user to a page specific to that listing where all the details about it are displayed, including its current price. If the user is signed in, they can also:
  - Add/Remove the item to/from their "watchlist".
  - Bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
  - Close the listing, if they are its owner. This makes the highest bidder win, rendering the listing inactive.
  - See if they have won the auction on a closed listing.
  - Add comments to the listing page. All comments made on a listing are be displayed.
- **Watchlist**: Every signed in user can visit a page that includes all the listings they have added to their watchlist. Clicking on any of them takes the user to that listing's page.
- **Categories**: Users can visit a page that displays all of the available categories. Clicking on the name of any category takes the user to a page that displays all active listings of that category.
- **User listings**: Users can visit a page where they can see all of their listings.
- **User Bids**: Users can visit a page where they can see all of the listings they have bid on.
- **Django admin interface**: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.
- **Models**: The application includes the following model classes that handle the database: Listing, Bid, Comment, Watching.
- **ModelForms**: The application also includes the following modelform classes that handle form generation: PartialListingForm, PartialCommentForm, PartialBidForm.

### What I implemented
This application's distribution code is available at: https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip (accessed 12 March 2026). It includes only the following routes: login, logout and register as well as a basic HTML layout for the navigation bar, the login and registration form. I studied, understood them and then moved on to complete the rest of the app. Specifically, I implemented the following:
- **Routes (views)**: All the other routes of the website (10)
- **Models**: all of the models classes.
- **ModelForms**: all of the modelforms classes.
- **HTML templates**: I substantially extended the existing HTML templates and added new ones for all the views and some error codes, using the appropriate semantic HTML elements.
- **CSS styles**: I implemented the entirety of the styles.css file (except a one-line rule) which is linked in every template. The file makes up a straightforward, organized style and layout. It is consistent with the responsive design principles, including flex-box and relative sizing utilities.

### What I learned
While working on this application I studied the Django documentation in depth and went beyond the basic requirements given by the course staff. Through this process I: 
- Deepened my understanding of Python's object-oriented programming concepts.
- Understood and applied modelforms in order to achieve systematic form generation from the relevant database fields.
- Developed experience researching and understanding framework documentation.
- Learned the importance of encapsulating the business logic related to the application's data within Django model classes.   
