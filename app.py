"""
This is a food delivery webapp, and you need an id and password to use the site.
Either you can register using registration link, or use the default id and password below:

id: admin
password: admin
"""


from flask import Flask, render_template, session, redirect, url_for, request, g
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, FoodSearch, CheckoutForm, CommentForm
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisp-is-my-secret-key"
app.config["SESSION_PERMANANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)


@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This is a food delivery webapp, and you need an id and password to use the site.
    Either you can register using registration link, or use the default id and password below:

    id: admin
    password: admin
    """
    if g.user is None:
        user = "Fellow Foodie"
    else:
        user = g.user
    form = FoodSearch()
    foods = None
    if form.validate_on_submit():
        dish = form.dish.data.upper()
        restaurant = form.restaurant.data
        db = get_db()
        if dish != "" and restaurant == "Select a Restaurant":
            foods = db.execute("""SELECT * FROM foods
                                WHERE name = ?""", (dish,)).fetchall()
        elif dish == "" and restaurant != "Select a Restaurant":
            foods = db.execute("""SELECT * FROM foods
                                WHERE Restaurant = ?""", (restaurant,)).fetchall()
        else:
            foods = db.execute("""SELECT * FROM foods""").fetchall()
    return render_template("index.html", foods=foods, form=form, user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        if db.execute("""SELECT * FROM users
                        WHERE user_id = ?;""", (user_id,)).fetchone() is not None:
            form.user_id.errors.append("User id is already taken")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                                            VALUES(?, ?);""", (user_id, generate_password_hash(password)))
            db.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute("""SELECT * FROM users
                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("Unknown user id")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/foods")
def foods():
    db = get_db()
    foods = db.execute("""SELECT * FROM foods;""").fetchall()
    return render_template("foods.html", foods=foods)


@app.route("/food/<int:food_id>", methods=["GET", "POST"])
def food(food_id):
    db = get_db()
    food = db.execute("""SELECT * FROM foods
                        WHERE food_id = ?;""", (food_id,)).fetchone()
    feedbacks = db.execute("""SELECT * FROM comments
                        WHERE food_id = ?;""", (food_id,)).fetchall()
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data
        feedbacks = db.execute(
            """INSERT INTO comments (food_id, name, comment) VALUES(?, ?, ?)""", (food_id, name, comment))
        db.commit()
        feedbacks = db.execute("""SELECT * FROM comments
                        WHERE food_id = ?;""", (food_id,)).fetchall()
        return render_template("food.html", food=food, form=form, feedbacks=feedbacks)
    return render_template("food.html", food=food, form=form, feedbacks=feedbacks)


@app.route("/basket", methods=["GET", "POST"])
@login_required
def basket():
    if "basket" not in session:
        session["basket"] = {}
    names = {}
    price = {}
    db = get_db()
    for food_id in session["basket"]:
        name = db.execute("""SELECT * FROM foods
                            WHERE food_id = ?""", (food_id,)).fetchone()["name"]
        names[food_id] = name
        dish_price = db.execute("""SELECT * FROM foods
                                WHERE name = ?""", (name,)).fetchone()["price"]
        price[food_id] = dish_price
    total = sum(price[a] * session["basket"][a] for a in price)
    form = CheckoutForm()
    if form.validate_on_submit():
        session["basket"].clear()
        return render_template("confirm.html")
    return render_template("basket.html", basket=session["basket"], price=price, total=total, names=names, form=form)


@ app.route("/add_to_basket/<int:food_id>")
@login_required
def add_to_basket(food_id):
    if "basket" not in session:
        session["basket"] = {}
    if food_id not in session["basket"]:
        session["basket"][food_id] = 0
    session["basket"][food_id] = session["basket"][food_id] + 1
    return redirect(url_for("basket"))


@ app.route("/less_to_basket/<int:food_id>")
@login_required
def less_to_basket(food_id):
    if "basket" not in session:
        session["basket"] = {}
    if food_id not in session["basket"]:
        session["basket"][food_id] = 0
    session["basket"][food_id] = session["basket"][food_id] - 1
    return redirect(url_for("basket"))


@app.route("/delete_food/<int:food_id>")
@login_required
def delete_food(food_id):
    del session["basket"][food_id]
    return redirect(url_for("basket"))


@app.route("/clear_basket")
@login_required
def clear_basket():
    session["basket"].clear()
    return redirect(url_for("basket"))


"""
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    address = None
    phone = None
    if form.validate_on_submit():
        address = form.address.data
        phone = form.phone.data
    return render_template("checkout.html", address=address, phone=phone, form=form)
"""
