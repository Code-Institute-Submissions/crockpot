import os
import re
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
recipes = mongo.db.recipes

now = datetime.now()
date_string = now.strftime("%d/%m/%Y")


@app.route("/")
def index():
    featured_recipes = recipes.find().skip(recipes.count() - 3)
    return render_template("index.html", featured_recipes=featured_recipes)


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
    fav_recipes = mongo.db.recipes.find({"is_fav": username})

    if session["user"]:
        return render_template("profile.html",
                               username=username, my_recipes=my_recipes,
                               fav_recipes=fav_recipes)

    return redirect(url_for("login"))


@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    if request.method == "POST":
        is_fav = [session["user"]] if request.form.get("is_fav") else []

        ingredient_names = request.form.getlist("ingredient_name")
        ingredient_names_reformat = []
        for ingredient in ingredient_names:
            ingredient_new = ingredient.lower().title().replace(' ', '')
            ingredient_names_reformat.append(ingredient_new)

        recipe = {
            "recipe_name": request.form.get("recipe_name").lower(),
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooktime"),
            "image_url": request.form.get("image_url"),
            "ingredient_name": ingredient_names_reformat,
            "ingredient_quantity": request.form.getlist("ingredient_quantity"),
            "ingredient_unit": request.form.getlist("ingredient_unit"),
            "instructions": request.form.getlist("instructions"),
            "source": request.form.get("source"),
            "tips": request.form.get("tips"),
            "created_by": session["user"],
            "date_added": date_string,
            "is_menu": [],
            "is_fav": is_fav
        }
        mongo.db.recipes.insert_one(recipe)
        flash(recipe.get("recipe_name") + " successfully added")

        return redirect(url_for(
                        "profile", username=session["user"]))

    return render_template("addRecipe.html")


@app.route("/editRecipe/<recipe_id>", methods=["GET", "POST"])
def editRecipe(recipe_id):
    if request.method == "POST":
        ingredient_names = request.form.getlist("ingredient_name")
        ingredient_names_reformat = []
        for ingredient in ingredient_names:
            ingredient_new = ingredient.lower().title().replace(' ', '')
            ingredient_names_reformat.append(ingredient_new)

        edit = {'$set': {
            "recipe_name": request.form.get("recipe_name").lower(),
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooktime"),
            "image_url": request.form.get("image_url"),
            "ingredient_name": ingredient_names_reformat,
            "ingredient_quantity": request.form.getlist("ingredient_quantity"),
            "ingredient_unit": request.form.getlist("ingredient_unit"),
            "instructions": request.form.getlist("instructions"),
            "source": request.form.get("source"),
            "tips": request.form.get("tips")
        }}
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edit)
        username = session["user"]
        recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
        recipe_is_fav = recipe.get("is_fav")
        if request.form.get("is_fav"):
            # If fav toggle is on and username in fav array do nothing
            if username in recipe_is_fav:
                pass
            # If fav toggle is on and username is not in fav array add username
            else:
                recipes.update_one({"_id": ObjectId(recipe_id)},
                                   {'$push': {"is_fav": username}})
        else:
            # If fav toggle is off and username in fav array remove username
            if username in recipe_is_fav:
                recipes.update_one({"_id": ObjectId(recipe_id)},
                                   {'$pull': {"is_fav": username}})
            # If fav toggle is off and username is not in fav array do nothing
            else:
                pass

        flash(recipe.get("recipe_name") + " successfully updated")
        return redirect(url_for(
                        "profile", username=session["user"]))

    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = zip(recipe["ingredient_name"],
                      recipe["ingredient_quantity"],
                      recipe["ingredient_unit"])
    return render_template(
        "editRecipe.html", recipe=recipe, ingredients=ingredients)


@app.route("/isMenu/<recipe_id>", methods=["GET", "POST"])
def isMenu(recipe_id):
    username = session["user"]
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    recipe_is_menu = recipe.get("is_menu")
    if request.method == "POST":
        if username in recipe_is_menu:
            recipes.update_one({"_id": ObjectId(recipe_id)},
                               {'$pull': {"is_menu": username}})
            flash(recipe.get("recipe_name") + " removed from menu")
        else:
            recipes.update_one({"_id": ObjectId(recipe_id)},
                               {'$push': {"is_menu": username}})
            flash(recipe.get("recipe_name") + " added to menu")

    return redirect(url_for("menu"))


@app.route("/isFav/<recipe_id>", methods=["GET", "POST"])
def isFav(recipe_id):
    username = session["user"]
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    recipe_is_fav = recipe.get("is_fav")
    if request.method == "POST":
        if request.form.get("is_favourite"):
            # If fav toggle is on and username in fav array do nothing
            if username in recipe_is_fav:
                pass
            # If fav toggle is on and username is not in fav array add username
            else:
                recipes.update_one({"_id": ObjectId(recipe_id)},
                                   {'$push': {"is_fav": username}})
            flash(recipe.get("recipe_name") + " added to favourites")
        else:
            # If fav toggle is off and username in fav array remove username
            if username in recipe_is_fav:
                recipes.update_one({"_id": ObjectId(recipe_id)},
                                   {'$pull': {"is_fav": username}})
            # If fav toggle is off and username is not in fav array do nothing
            else:
                pass
            flash(recipe.get("recipe_name") + " removed from favourites")

        return redirect(url_for(
                        "profile", username=session["user"]))


@app.route("/deleteRecipe/<recipe_id>")
def deleteRecipe(recipe_id):
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    recipe_name = recipe.get("recipe_name")
    recipes.remove({"_id": ObjectId(recipe_id)})
    flash(recipe_name + " successfully deleted")

    return redirect(url_for(
                        "profile", username=session["user"]))


@app.route("/viewRecipe/<recipe_id>")
def viewRecipe(recipe_id):
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})

    ingredient_names = recipe["ingredient_name"]
    ingredient_names_reformat = []
    for ingredient in ingredient_names:
        # https://stackoverflow.com/questions/25674532/pythonic-way-to-add-space-before-capital-letter-if-and-only-if-previous-letter-i/25674575
        ingredient_new = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', ingredient)
        ingredient_names_reformat.append(ingredient_new)

    ingredients = zip(ingredient_names_reformat,
                      recipe["ingredient_quantity"],
                      recipe["ingredient_unit"])

    return render_template(
        "viewRecipe.html", recipe=recipe, ingredients=ingredients)


# Resets search results
@app.route("/searchRecipe")
def searchReset():
    search_recipes = recipes.find()
    search_ingredients = []

    for recipe in search_recipes:
        search_ingredients.extend(recipe["ingredient_name"])

    search_ingredients = list(dict.fromkeys(search_ingredients))

    search_ingredients_reformat = []
    for ingredient in search_ingredients:
        # https://stackoverflow.com/questions/25674532/pythonic-way-to-add-space-before-capital-letter-if-and-only-if-previous-letter-i/25674575
        ingredient_new = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', ingredient)
        search_ingredients_reformat.append(ingredient_new)

    search_ingredients = search_ingredients_reformat

    search_recipes = recipes.find()
    return render_template("searchRecipe.html", search_recipes=search_recipes,
                           search_ingredients=(sorted(search_ingredients)))


# New search
@app.route("/searchRecipe", methods=["GET", "POST"])
def search():
    search_recipes = recipes.find()
    search_ingredients = []

    for recipe in search_recipes:
        search_ingredients.extend(recipe["ingredient_name"])

    search_ingredients = list(dict.fromkeys(search_ingredients))

    search_ingredients_reformat = []
    for ingredient in search_ingredients:
        # https://stackoverflow.com/questions/25674532/pythonic-way-to-add-space-before-capital-letter-if-and-only-if-previous-letter-i/25674575
        ingredient_new = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', ingredient)
        search_ingredients_reformat.append(ingredient_new)

    search_ingredients = search_ingredients_reformat

    query = request.form.get("query")
    search_recipes = recipes.find({"$text": {"$search": query}})
    print(({"$text": {"$search": query}}))
    return render_template("searchRecipe.html", search_recipes=search_recipes,
                           search_ingredients=(sorted(search_ingredients)))


@app.route("/menu")
def menu():
    # name = n
    # quantity = q
    # unit = u
    menu_recipes = recipes.find({"is_menu": session["user"]})
    menu_ingredients = []
    menu_ingredient_ns = []
    menu_ingredient_qs = []
    menu_ingredient_us = []

    for recipe in menu_recipes:
        recipe_ingredient_ns = recipe["ingredient_name"]
        recipe_ingredient_qs = recipe["ingredient_quantity"]
        recipe_ingredient_us = recipe["ingredient_unit"]
        i = 0
        imax = len(recipe_ingredient_ns) - 1

        # Iterate through all ingredients names and corresponding quantities
        # and units for each recipe
        while i <= imax:
            recipe_ingredient_n = recipe_ingredient_ns[i]
            recipe_ingredient_q = recipe_ingredient_qs[i]
            recipe_ingredient_u = recipe_ingredient_us[i]

            # If ingredient name has already been added to list of menu
            # ingredients names...
            if recipe_ingredient_n in menu_ingredient_ns:
                # ...find index of matching ingredient name
                index = menu_ingredient_ns.index(recipe_ingredient_n)
                # ...find quantities and units of matching ingredients
                quantityOne = int(menu_ingredient_qs[index])
                quantityTwo = int(recipe_ingredient_q)
                unitOne = menu_ingredient_us[index]
                unitTwo = recipe_ingredient_u
                # If the units of the two matching ingredients are the same,
                # sum the quantities and don't add ingredients name to list
                if unitOne == unitTwo:
                    menu_ingredient_qs[index] = quantityOne + quantityTwo
                # If the units of the two matching ingredients are not the
                # same, do not sum the quantities and add ingredients name
                # to list
                else:
                    menu_ingredient_ns.append(recipe_ingredient_n)
                    menu_ingredient_qs.append(recipe_ingredient_q)
                    menu_ingredient_us.append(recipe_ingredient_u)
                i += 1
            # If ingredient name is not on list of menu ingredients names add
            # ingredients name to list
            else:
                menu_ingredient_ns.append(recipe_ingredient_n)
                menu_ingredient_qs.append(recipe_ingredient_q)
                menu_ingredient_us.append(recipe_ingredient_u)
                i += 1

    # Put menu ingredient names, quantities and
    # units into new list and sort alphabetically
    j = 0
    jmax = len(menu_ingredient_ns) - 1

    while j <= jmax:
        menu_ingredients.append([menu_ingredient_ns[j],
                                 menu_ingredient_qs[j],
                                 menu_ingredient_us[j]])
        j += 1

    menu_ingredients = (sorted(menu_ingredients, key=lambda x: x[0]))

    menu_recipes = recipes.find({"is_menu": session["user"]})
    return render_template(
        "menu.html", menu_recipes=menu_recipes,
        menu_ingredients=menu_ingredients)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to false when submitting
            debug=True)
