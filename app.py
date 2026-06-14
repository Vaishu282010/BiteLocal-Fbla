# BiteLocal - a website to find local restaurants in Louisville
# made for FBLA Coding and Programming 2025-2026
# topic is Byte-Sized Business Boost
# by: vaishu and Ash from Eastern High School

# we used python because thats what we learned in class
# flask is what makes the website work with multiple pages
# we watched some youtube tutorials to figure out the session stuff

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import re
import random

app = Flask(__name__)
app.secret_key = "bitelocal2025secret"

# Restaurant Data
RESTAURANTS = [
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

RESTAURANT_INDEX = {r["id"]: r for r in RESTAURANTS}
reviews = {r["id"]: [] for r in RESTAURANTS}
submissions = []

def get_avg_rating(rid ):
    rv = reviews.get(rid, [])
    if not rv: return 0
    return round(sum(r["rating"] for r in rv) / len(rv), 1)

def add_ratings(restaurant_list):
    result = []
    for r in restaurant_list:
        r2 = dict(r)
        r2["avg_rating"] = get_avg_rating(r["id"])
        r2["review_count"] = len(reviews.get(r["id"], []))
        result.append(r2)
    return result

def get_bookmarks():
    return session.get("bookmarks", [])

def check_name(val):
    val = val.strip()
    if len(val) < 2: return "Name needs to be at least 2 characters"
    if len(val) > 100: return "Name is too long"
    if re.search(r"[<>\"'&]", val): return "Name has characters that aren't allowed"
    if val.isdigit(): return "That doesn't look like a real name"
    return None

def check_email(val):
    val = val.strip()
    if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", val):
        return "Email doesn't look right, try something like name@gmail.com"
    if val.lower() in ["test@test.com", "fake@fake.com", "a@a.com", "email@email.com"]:
        return "Please use a real email"
    return None

def check_rating(val):
    try:
        n = int(val)
        if n < 1 or n > 5: return "Rating has to be between 1 and 5"
    except: return "Please pick a star rating"
    return None

def make_captcha():
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    session["captcha_answer"] = num1 + num2
    return f"{num1} + {num2}"

def check_captcha(val):
    try:
        if int(val) == session.get("captcha_answer"): return None
        return "Incorrect verification answer. Please try again."
    except: return "Please enter a valid number for verification."

@app.route("/")
def home():
    return render_template("index.html", restaurants=add_ratings(RESTAURANTS))

@app.route("/browse")
def browse():
    category = request.args.get("category", "all")
    sort_by = request.args.get("sort", "name")
    search = request.args.get("search", "").strip().lower()
    pool = [r for r in RESTAURANTS if category == "all" or r["category"] == category]
    if search:
        pool = [r for r in pool if search in r["name"].lower() or search in r["description"].lower() or search in r["location"].lower()]
    pool = add_ratings(pool)
    if sort_by == "rating": pool.sort(key=lambda x: x["avg_rating"], reverse=True)
    elif sort_by == "price_low": pool.sort(key=lambda x: len(x["price"]))
    else: pool.sort(key=lambda x: x["name"].lower())
    return render_template("browse.html", restaurants=pool, category=category, sort_by=sort_by, search=search, bookmarks=get_bookmarks())

@app.route("/restaurant/<rid>")
def detail(rid):
    restaurant = RESTAURANT_INDEX.get(rid)
    if not restaurant:
        flash("Couldn't find that restaurant!", "error")
        return redirect(url_for("browse"))
    return render_template("detail.html", restaurant=restaurant, restaurant_reviews=reviews.get(rid, []), avg_rating=get_avg_rating(rid), bookmarks=get_bookmarks(), captcha_question=make_captcha())

@app.route("/review/<rid>", methods=["POST"])
def submit_review(rid):
    author, rating, comment, captcha = request.form.get("author", "").strip(), request.form.get("rating", "").strip(), request.form.get("comment", "").strip(), request.form.get("captcha", "").strip()
    errors = [e for e in [check_name(author), check_rating(rating), check_captcha(captcha)] if e]
    if len(comment) > 400: errors.append("Comment is too long")
    if errors:
        for e in errors: flash(e, "error")
        return redirect(url_for("detail", rid=rid))
    reviews[rid].append({"author": author, "rating": int(rating), "comment": comment, "date": datetime.now().strftime("%b %d, %Y")})
    flash("Review posted! Thanks :)", "success")
    return redirect(url_for("detail", rid=rid))

@app.route("/bookmark/<rid>", methods=["POST"])
def bookmark(rid):
    if rid not in RESTAURANT_INDEX: return redirect(url_for("browse"))
    bmarks = get_bookmarks()
    if rid in bmarks: bmarks.remove(rid)
    else: bmarks.append(rid)
    session["bookmarks"] = bmarks
    return redirect(request.referrer or url_for("browse"))

@app.route("/bookmarks")
def bookmarks_page():
    saved = [RESTAURANT_INDEX[i] for i in get_bookmarks() if i in RESTAURANT_INDEX]
    return render_template("bookmarks.html", restaurants=add_ratings(saved))

@app.route("/deals")
def deals():
    return render_template("deals.html", restaurants=add_ratings(RESTAURANTS))

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name, email, category, location, description, captcha = request.form.get("name", "").strip(), request.form.get("email", "").strip(), request.form.get("category", "").strip(), request.form.get("location", "").strip(), request.form.get("description", "").strip(), request.form.get("captcha", "").strip()
        errors = [e for e in [check_name(name), check_email(email), check_captcha(captcha)] if e]
        if not category: errors.append("Please pick a category")
        if len(location) < 3: errors.append("Please enter a location")
        if errors:
            for e in errors: flash(e, "error")
            return render_template("submit.html", form_data=request.form, captcha_question=make_captcha())
        submissions.append({"name": name, "email": email, "category": category, "location": location, "description": description, "date": datetime.now().strftime("%b %d, %Y")})
        flash("Thanks! We got your submission :)", "success")
        return redirect(url_for("submit"))
    return render_template("submit.html", form_data={}, captcha_question=make_captcha())

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/sources")
def sources(): return render_template("sources.html")

@app.route("/report")
def report():
    category_counts = {}
    for r in RESTAURANTS: category_counts[r["category"]] = category_counts.get(r["category"], 0) + 1
    all_rated = [r for r in add_ratings(RESTAURANTS) if r["review_count"] > 0]
    all_rated.sort(key=lambda x: x["avg_rating"], reverse=True)
    return render_template("report.html", category_counts=category_counts, top_restaurants=all_rated[:5], total_reviews=sum(len(v) for v in reviews.values()), submissions=submissions, total_restaurants=len(RESTAURANTS))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
