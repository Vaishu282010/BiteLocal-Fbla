# BiteLocal - a website to find local restaurants in Louisville
# made for FBLA Coding and Programming 2025-2026
# topic is Byte-Sized Business Boost
# by: [Vaishu] and [Ash] from [Eastern high school]
# we used python because thats what we learned in class
# flask is what makes the website work with multiple pages
# we watched some youtube tutorials to figure out the session stuff

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import re

app = Flask(__name__)
# this is needed for sessions and flash messages to work
app.secret_key = "bitelocal2025secret"



# we added website links so people can look up the real place
RESTAURANTS = [
    # american food
    {
        "id": "burger-barn",
        "name": "Burger Barn",
        "category": "american",
        "description": "Classic smash burgers and hand-cut fries made fresh daily. A Louisville staple since 2005.",
        "location": "Downtown Louisville, KY",
        "price": "$",
        "deal": "Buy 1 burger get free fries on Tuesdays!",
        "deal_code": "BURGER2FOR1",
        "website": "https://www.yelp.com/search?find_desc=burgers&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80",
    },
    {
        "id": "liberty-grill",
        "name": "Liberty Grill",
        "category": "american",
        "description": "BBQ ribs, pulled pork, and homemade mac and cheese slow cooked every day.",
        "location": "Highlands, Louisville KY",
        "price": "$$",
        "deal": "10% off for students with school ID",
        "deal_code": "STUDENT10",
        "website": "https://www.yelp.com/search?find_desc=bbq&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&q=80",
    },
    {
        "id": "mama-jeans",
        "name": "Mama Jean's Diner",
        "category": "american",
        "description": "Old school diner with breakfast all day and homemade pies baked fresh every morning.",
        "location": "St. Matthews, Louisville KY",
        "price": "$",
        "deal": "Free coffee refills every morning before 10am",
        "deal_code": "MORNINGCOFFEE",
        "website": "https://www.yelp.com/search?find_desc=diner&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400&q=80",
    },
    {
        "id": "smokehouse-lou",
        "name": "Smokehouse Lou",
        "category": "american",
        "description": "Slow smoked brisket, ribs, and classic southern sides cooked low and slow.",
        "location": "Portland, Louisville KY",
        "price": "$$",
        "deal": "Free side dish with any full rack order",
        "deal_code": "SMOKESIDE",
        "website": "https://www.yelp.com/search?find_desc=smokehouse&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&q=80",
    },
    # italian food
    {
        "id": "nonna-pasta",
        "name": "Nonna's Pasta House",
        "category": "italian",
        "description": "Homemade pasta, wood-fired pizza, and the best tiramisu in Louisville.",
        "location": "NuLu, Louisville KY",
        "price": "$$",
        "deal": "Half price pasta on Monday nights",
        "deal_code": "MONDAYPASTA",
        "website": "https://www.yelp.com/search?find_desc=italian+pasta&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&q=80",
    },
    {
        "id": "pizza-palace",
        "name": "Pizza Palace",
        "category": "italian",
        "description": "New York style pizza by the slice or whole pie. 20+ toppings available.",
        "location": "Bardstown Rd, Louisville KY",
        "price": "$",
        "deal": "Large pizza for $10 every Friday night",
        "deal_code": "FRIDAYPIE",
        "website": "https://www.yelp.com/search?find_desc=pizza&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&q=80",
    },
    {
        "id": "tuscan-table",
        "name": "Tuscan Table",
        "category": "italian",
        "description": "Fancy Italian with risotto, seafood pasta, and a great wine list.",
        "location": "East End, Louisville KY",
        "price": "$$$",
        "deal": "Free dessert on your birthday - just show your ID!",
        "deal_code": "BDAYDESSERT",
        "website": "https://www.yelp.com/search?find_desc=tuscan+italian&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&q=80",
    },
    {
        "id": "luigi-calzone",
        "name": "Luigi's Calzone Corner",
        "category": "italian",
        "description": "Stuffed calzones, stromboli, and garlic knots baked fresh all day.",
        "location": "Shively, Louisville KY",
        "price": "$",
        "deal": "Buy any calzone, get a free garlic knot basket",
        "deal_code": "CALZONEKNOT",
        "website": "https://www.yelp.com/search?find_desc=calzone&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&q=80",
    },
    # asian food
    {
        "id": "dragon-wok",
        "name": "Dragon Wok",
        "category": "asian",
        "description": "Chinese takeout with lo mein, fried rice, and handmade dumplings.",
        "location": "Crescent Hill, Louisville KY",
        "price": "$",
        "deal": "Free egg roll with any order over $15",
        "deal_code": "EGGROLL15",
        "website": "https://www.yelp.com/search?find_desc=chinese+food&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&q=80",
    },
    {
        "id": "sakura-sushi",
        "name": "Sakura Sushi",
        "category": "asian",
        "description": "Fresh sushi rolls, ramen bowls, and Japanese appetizers made to order.",
        "location": "Middletown, Louisville KY",
        "price": "$$",
        "deal": "Happy hour sushi 4-6pm weekdays - 20% off everything",
        "deal_code": "HAPPYHOUR20",
        "website": "https://www.yelp.com/search?find_desc=sushi&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&q=80",
    },
    {
        "id": "pho-saigon",
        "name": "Pho Saigon",
        "category": "asian",
        "description": "Authentic Vietnamese pho, banh mi sandwiches, and fresh spring rolls.",
        "location": "South End, Louisville KY",
        "price": "$",
        "deal": "Free bubble tea with any large pho bowl",
        "deal_code": "BUBBLETEA",
        "website": "https://www.yelp.com/search?find_desc=vietnamese+pho&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=400&q=80",
    },
    {
        "id": "thai-orchid",
        "name": "Thai Orchid",
        "category": "asian",
        "description": "Authentic Thai curries, pad thai, and mango sticky rice dessert.",
        "location": "Cherokee Triangle, Louisville KY",
        "price": "$$",
        "deal": "Free spring rolls with orders over $20",
        "deal_code": "THAISPRING",
        "website": "https://www.yelp.com/search?find_desc=thai+food&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1562802378-063ec186a863?w=400&q=80",
    },
    # mexican food
    {
        "id": "taco-fiesta",
        "name": "Taco Fiesta",
        "category": "mexican",
        "description": "Street tacos, burritos, and fresh guacamole made right in front of you.",
        "location": "Germantown, Louisville KY",
        "price": "$",
        "deal": "Taco Tuesday - 3 tacos for $5 all day!",
        "deal_code": "TACOTUESDAY",
        "website": "https://www.yelp.com/search?find_desc=tacos&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&q=80",
    },
    {
        "id": "casa-grande",
        "name": "Casa Grande",
        "category": "mexican",
        "description": "Sit-down Mexican restaurant with sizzling fajitas and fresh margaritas.",
        "location": "Okolona, Louisville KY",
        "price": "$$",
        "deal": "Kids eat free every Sunday with adult entree",
        "deal_code": "SUNDAYKIDS",
        "website": "https://www.yelp.com/search?find_desc=mexican+restaurant&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=400&q=80",
    },
    {
        "id": "el-rancho",
        "name": "El Rancho Grill",
        "category": "mexican",
        "description": "Tex-Mex with loaded nachos, enchiladas, and an all-you-can-eat salsa bar.",
        "location": "Newburg, Louisville KY",
        "price": "$",
        "deal": "Free chips and salsa with every table - no purchase needed",
        "deal_code": "FREECHIPS",
        "website": "https://www.yelp.com/search?find_desc=tex+mex&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=400&q=80",
    },
    # desserts
    {
        "id": "sweet-scoops",
        "name": "Sweet Scoops Ice Cream",
        "category": "desserts",
        "description": "Local ice cream shop with 40+ flavors and homemade waffle cones.",
        "location": "Clifton, Louisville KY",
        "price": "$",
        "deal": "Buy 2 scoops get 1 free every Wednesday",
        "deal_code": "WEDNESDAY3",
        "website": "https://www.yelp.com/search?find_desc=ice+cream&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400&q=80",
    },
    {
        "id": "the-cake-shop",
        "name": "The Cake Shop",
        "category": "desserts",
        "description": "Custom cakes, cupcakes, and pastries baked from scratch every morning.",
        "location": "Butchertown, Louisville KY",
        "price": "$$",
        "deal": "Free cupcake with any whole cake order",
        "deal_code": "FREECUPCAKE",
        "website": "https://www.yelp.com/search?find_desc=bakery+cakes&find_loc=Louisville%2C+KY",
        "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400&q=80",
    },
    {
        "id": "donut-den",
        "name": "The Donut Den",
        "category": "desserts",
        "description": "Louisville's most famous donut shop. Over 30 flavors made fresh overnight.",
        "location": "Fern Creek, Louisville KY",
        "price": "$",
        "deal": "Buy a dozen get 2 free donuts",
        "deal_code": "DOZEN2FREE",
        "website": "https://donutden.com",
        "img": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=400&q=80",
    },
]

# this makes it easy to find a restaurant by its id really fast
# basically like a lookup table
RESTAURANT_INDEX = {}
for r in RESTAURANTS:
    RESTAURANT_INDEX[r["id"]] = r

# we store all reviews in memory  like a dictionary
# each key is a restaurant id and the value is a list of review dicts
reviews = {}
for r in RESTAURANTS:
    reviews[r["id"]] = []

# list to store restaurants people submit
submissions = []


# helper function to get the average star rating for a restaurant
def get_avg_rating(rid):
    rv = reviews[rid]
    if len(rv) == 0:
        return 0
    total = 0
    for r in rv:
        total = total + r["rating"]
    avg = total / len(rv)
    return round(avg, 1)


# this adds avg_rating and review_count to each restaurant in a list
# we use it a lot so we made it a function
def add_ratings(restaurant_list):
    result = []
    for r in restaurant_list:
        r2 = dict(r)  # make a copy so we dont change the original
        r2["avg_rating"] = get_avg_rating(r["id"])
        r2["review_count"] = len(reviews[r["id"]])
        result.append(r2)
    return result


# get saved restaurants from the browser session
def get_bookmarks():
    return session.get("bookmarks", [])


# check if a name is valid
# syntactic: checks length and format
# semantic: checks it isnt just numbers
def check_name(val):
    val = val.strip()
    if len(val) < 2:
        return "Name needs to be at least 2 characters"
    if len(val) > 100:
        return "Name is too long"
    if re.search(r"[<>\"'&]", val):
        return "Name has characters that aren't allowed"
    if val.isdigit():
        return "That doesn't look like a real name"
    return None


# check if email looks real
def check_email(val):
    val = val.strip()
    # regex to check email format
    if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", val):
        return "Email doesn't look right, try something like name@gmail.com"
    # reject obviously fake ones
    fake = ["test@test.com", "fake@fake.com", "a@a.com", "email@email.com"]
    if val.lower() in fake:
        return "Please use a real email"
    return None


# make sure rating is 1-5
def check_rating(val):
    try:
        n = int(val)
        if n < 1 or n > 5:
            return "Rating has to be between 1 and 5"
    except:
        return "Please pick a star rating"
    return None


# home page
@app.route("/")
def home():
    all_restaurants = add_ratings(RESTAURANTS)
    return render_template("home.html", restaurants=all_restaurants)


# browse page - has search, filter, and sort
@app.route("/browse")
def browse():
    category = request.args.get("category", "all")
    sort_by = request.args.get("sort", "name")
    search = request.args.get("search", "").strip().lower()

    # filter by category first
    if category == "all":
        pool = list(RESTAURANTS)
    else:
        pool = []
        for r in RESTAURANTS:
            if r["category"] == category:
                pool.append(r)

    # then filter by search if they typed something
    # this searches the name, description, and location
    if search:
        filtered = []
        for r in pool:
            if search in r["name"].lower():
                filtered.append(r)
            elif search in r["description"].lower():
                filtered.append(r)
            elif search in r["location"].lower():
                filtered.append(r)
        pool = filtered

    # add ratings before sorting
    pool = add_ratings(pool)

    # sort the list
    if sort_by == "rating":
        pool.sort(key=lambda x: x["avg_rating"], reverse=True)
    elif sort_by == "price_low":
        pool.sort(key=lambda x: len(x["price"]))
    else:
        pool.sort(key=lambda x: x["name"].lower())

    return render_template("browse.html",
        restaurants=pool,
        category=category,
        sort_by=sort_by,
        search=search,
        bookmarks=get_bookmarks()
    )


# single restaurant detail page
@app.route("/restaurant/<rid>")
def detail(rid):
    restaurant = RESTAURANT_INDEX.get(rid)
    if not restaurant:
        flash("Couldn't find that restaurant!", "error")
        return redirect(url_for("browse"))

    restaurant_reviews = reviews.get(rid, [])
    avg = get_avg_rating(rid)

    return render_template("detail.html",
        restaurant=restaurant,
        restaurant_reviews=restaurant_reviews,
        avg_rating=avg,
        bookmarks=get_bookmarks()
    )


# handle review form submission
@app.route("/review/<rid>", methods=["POST"])
def submit_review(rid):
    # honeypot field - bots fill this in but real users cant see it
    if request.form.get("website", ""):
        flash("Bot detected!", "error")
        return redirect(url_for("detail", rid=rid))

    author = request.form.get("author", "").strip()
    rating = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()

    # collect all errors
    errors = []
    e1 = check_name(author)
    e2 = check_rating(rating)
    if e1:
        errors.append(e1)
    if e2:
        errors.append(e2)
    if len(comment) > 400:
        errors.append("Comment is too long, keep it under 400 characters")

    if len(errors) > 0:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("detail", rid=rid))

    # save the review
    reviews[rid].append({
        "author": author,
        "rating": int(rating),
        "comment": comment,
        "date": datetime.now().strftime("%b %d, %Y")
    })

    flash("Review posted! Thanks :)", "success")
    return redirect(url_for("detail", rid=rid))


# save or unsave a restaurant
@app.route("/bookmark/<rid>", methods=["POST"])
def bookmark(rid):
    if rid not in RESTAURANT_INDEX:
        flash("Restaurant not found", "error")
        return redirect(url_for("browse"))

    bmarks = get_bookmarks()

    if rid in bmarks:
        bmarks.remove(rid)
        flash("Removed from saved", "info")
    else:
        bmarks.append(rid)
        flash("Saved! ⭐", "success")

    session["bookmarks"] = bmarks
    # go back to wherever they were
    return redirect(request.referrer or url_for("browse"))


# saved restaurants page
@app.route("/bookmarks")
def bookmarks_page():
    ids = get_bookmarks()
    saved = []
    for i in ids:
        if i in RESTAURANT_INDEX:
            saved.append(RESTAURANT_INDEX[i])
    saved = add_ratings(saved)
    return render_template("bookmarks.html", restaurants=saved)


# deals page
@app.route("/deals")
def deals():
    return render_template("deals.html", restaurants=add_ratings(RESTAURANTS))


# submit a new restaurant form
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # bot check
        if request.form.get("website", ""):
            flash("Bot detected!", "error")
            return redirect(url_for("submit"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        # validate everything
        errors = []
        e1 = check_name(name)
        e2 = check_email(email)
        if e1:
            errors.append(e1)
        if e2:
            errors.append(e2)
        if not category:
            errors.append("Please pick a category")
        if len(location) < 3:
            errors.append("Please enter a location")
        if len(description) > 500:
            errors.append("Description is too long (max 500 characters)")

        if len(errors) > 0:
            for e in errors:
                flash(e, "error")
            return render_template("submit.html", form_data=request.form)

        # save submission
        submissions.append({
            "name": name,
            "email": email,
            "category": category,
            "location": location,
            "description": description,
            "date": datetime.now().strftime("%b %d, %Y")
        })

        flash("Thanks! We got your submission :)", "success")
        return redirect(url_for("submit"))

    return render_template("submit.html", form_data={})


# about page
@app.route("/about")
def about():
    return render_template("about.html")


# sources page
@app.route("/sources")
def sources():
    return render_template("sources.html")


# report page with stats
@app.route("/report")
def report():
    # count how many restaurants are in each category
    category_counts = {}
    for r in RESTAURANTS:
        cat = r["category"]
        if cat in category_counts:
            category_counts[cat] += 1
        else:
            category_counts[cat] = 1

    # get top rated (only ones with at least one review)
    all_rated = add_ratings(RESTAURANTS)
    with_reviews = []
    for r in all_rated:
        if r["review_count"] > 0:
            with_reviews.append(r)
    with_reviews.sort(key=lambda x: x["avg_rating"], reverse=True)

    total_reviews = 0
    for v in reviews.values():
        total_reviews += len(v)

    return render_template("report.html",
        category_counts=category_counts,
        top_restaurants=with_reviews[:5],
        total_reviews=total_reviews,
        submissions=submissions,
        total_restaurants=len(RESTAURANTS)
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
