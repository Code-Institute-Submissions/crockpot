import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("input-username-signup").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        signup = {
            "username": request.form.get("input-username-signup").lower(),
            "password": generate_password_hash(
                request.form.get("input-password-signup"))
        }
        mongo.db.users.insert_one(signup)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("input-username-signup").lower()
        flash("Registration Successful!")
    return render_template("signup.html")


@app.route("/addRecipe")
def addRecipe():
    return render_template("addRecipe.html")


@app.route("/viewRecipe")
def viewRecipe():
    recipes = mongo.db.recipes.find()
    return render_template("viewRecipe.html", recipes=recipes)


@app.route("/searchRecipe")
def searchRecipe():
    return render_template("searchRecipe.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to false when submitting
            debug=True)
