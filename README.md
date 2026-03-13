# BiteLocal - Local Restaurant Finder
## FBLA Coding & Programming 2025-2026
**Topic:** Byte-Sized Business Boost
**Made by:** Vaishnavi Bommalata & Ashrita Ambhore
**School:** Eastern high school

---

## What is BiteLocal?

BiteLocal is a web app that helps people in Louisville, KY find local restaurants.
You can browse by food type, search by name, writw read reviews, save favorites, and find
special deals. We made it for FBLA Coding and Programming because we thought a
restaurant finder was a good way to help boost small local businesses.

---

## How to Run the App

### Step 1 - Make sure Python is installed
Open PowerShell or Command Prompt and type:
```
python --version
```
You should see something like `Python 3.x.x`. If not, download Python from python.org.

### Step 2 - Install Flask
```
python -m pip install flask
```

### Step 3 - Run the app
```
python app.py
```

### Step 4 - Open in browser
Go to: **http://127.0.0.1:5000**

> Note: Keep the terminal open while using the app. Closing it stops the website.

---

## Features

- **Browse restaurants** — view all 17 local restaurants with photos, descriptions, and prices
- **Search** — search by restaurant name, description, or location
- **Filter by category** — American, Italian, Asian, Mexican, Desserts
- **Sort** — sort by name (A-Z), top rated, or cheapest first
- **Star ratings & reviews** — click stars to rate, write a comment, see all reviews
- **Bookmarks** — save restaurants to a personal list using browser sessions
- **Deals page** — every restaurant has a special deal and promo code you can claim
- **Website links** — each restaurant links to their page so you can learn more
- **Submit a restaurant** — users can submit new restaurants through a form
- **Data report page** — shows stats like total restaurants, top rated, and submissions

---

## Why We Used Python

We chose Python 3 because:
- We learned it in our CS class so we already knew the basics
- It is easy to read and understand
- Real companies like Instagram, Spotify, and Pinterest use Python
- Flask makes it easy to build a multi-page website without a lot of setup
- You can run the whole app with one command

We used Flask specifically because it is lightweight and good for beginner web projects.
Jinja2 templates (built into Flask) let us write the header and footer one time and
reuse them on every page, which follows the DRY principle (Don't Repeat Yourself).

---

## File Structure

```
bitelocal2/
├── app.py                  # main Python file, all routes and data
├── README.md               # this file
├── static/
│   └── style.css           # all the CSS styling
└── templates/
    ├── base.html           # shared header, nav, and footer
    ├── home.html           # home page with deals slideshow
    ├── browse.html         # browse/search/filter page
    ├── detail.html         # single restaurant page with reviews
    ├── deals.html          # all deals in one place
    ├── bookmarks.html      # saved restaurants
    ├── submit.html         # submit a new restaurant form
    ├── about.html          # about the project
    └── report.html         # data report and stats
```

---

## Security & Validation

### Bot Prevention
I added Captcha Bot verfication 
we know it was a bot and we reject the submission.

### Input Validation
We validate all user input before saving it. We check both:

**Syntactic validation** (is the format correct?):
- Names: must be 2-100 characters, no HTML characters like `< > " '`
- Emails: must match the regex pattern `name@domain.com`
- Ratings: must be a number that can be converted with `int()`

**Semantic validation** (does the value make sense?):
- Names: cannot be all digits (e.g. "12345" is not a real name)
- Emails: rejects known fake emails like `test@test.com` or `fake@fake.com`
- Ratings: must be between 1 and 5, not just any number

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python     | 3.x     | Main programming language |
| Flask      | 3.x     | Web framework for routing and templates |
| Jinja2     | built-in| HTML templating (comes with Flask) |
| CSS3       | -       | Styling and responsive design |
| Google Fonts | -     | Bebas Neue and Nunito fonts |
| Unsplash   | -       | Free food photography |

---

## What We Learned

- How to build a multi-page website with Flask
- How to use Jinja2 templates to avoid repeating code
- How Flask sessions work for storing user data like bookmarks
- How to validate form input
- How to use CSS and grid for layouts
- How honeypot fields work for bot prevention
- How to use Python dictionaries for fast lookups

---
*Made for FBLA Coding & Programming 2025-2026 | Byte-Sized Business Boost*
