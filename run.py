import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
users = mongo.db.user_login_system
recipes = mongo.db.recipes

now = datetime.now()
date_string = now.strftime("%d/%m/%Y")


@app.route("/")
def index():
    return render_template("index.html", featured_recipes=recipes.find())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("input-username-login").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get(
                    "input-password-login")):
                    session["user"] = request.form.get(
                        "input-username-login").lower()
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


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
                request.form.get("input-password-signup")),
            "is_favourite": ""
        }
        mongo.db.users.insert_one(signup)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("input-username-signup").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("signup.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    my_recipes = mongo.db.recipes.find({"created_by": username})
    fav_recipes = mongo.db.recipes.find({"is_favourite": "on"})

    if session["user"]:
        return render_template("profile.html",
                               username=username, my_recipes=my_recipes,
                               fav_recipes=fav_recipes)

    return redirect(url_for("login"))


@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    if request.method == "POST":
        is_favourite = "on" if request.form.get("is_favourite") else "off"
        recipe = {
            "recipe_name": request.form.get("recipe_name").lower(),
            "is_favourite": is_favourite,
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooktime"),
            "image_url": request.form.get("image_url"),
            "ingredient_name": request.form.getlist("ingredient_name"),
            "ingredient_quantity": request.form.getlist("ingredient_quantity"),
            "ingredient_unit": request.form.getlist("ingredient_unit"),
            "instructions": request.form.getlist("instructions"),
            "source": request.form.get("source"),
            "tips": request.form.get("tips"),
            "created_by": session["user"],
            "date_added": date_string
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added")
        return render_template("profile.html")

    return render_template("addRecipe.html")


@app.route("/editRecipe/<recipe_id>", methods=["GET", "POST"])
def editRecipe(recipe_id):
    if request.method == "POST":
        is_favourite = "on" if request.form.get("is_favourite") else "off"
        edit = {
            "recipe_name": request.form.get("recipe_name").lower(),
            "is_favourite": is_favourite,
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooktime"),
            "image_url": request.form.get("image_url"),
            "ingredient_name": request.form.getlist("ingredient_name"),
            "ingredient_quantity": request.form.getlist("ingredient_quantity"),
            "ingredient_unit": request.form.getlist("ingredient_unit"),
            "instructions": request.form.getlist("instructions"),
            "source": request.form.get("source"),
            "tips": request.form.get("tips"),
            "created_by": session["user"],
            "date_added": date_string
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edit)
        flash("Recipe Successfully Updated")

    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        "editRecipe.html", recipe=recipe)


@app.route("/viewRecipe/<recipe_id>")
def viewRecipe(recipe_id):
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = zip(recipe["ingredient_name"],
                      recipe["ingredient_quantity"],
                      recipe["ingredient_unit"])

    return render_template(
        "viewRecipe.html", recipe=recipe, ingredients=ingredients)


@app.route("/searchRecipe")
def searchRecipe():
    return render_template("searchRecipe.html", all_recipes=recipes.find())


@app.route("/menu")
def menu():
    return render_template("menu.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to false when submitting
            debug=True)
