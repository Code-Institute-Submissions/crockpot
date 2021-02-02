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
        recipe = {
            "recipe_name": request.form.get("recipe_name").lower(),
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
            "date_added": date_string,
            "is_menu": [],
            "is_fav": is_fav
        }
        mongo.db.recipes.insert_one(recipe)
        flash(recipe.get("recipe_name") + " Successfully Added")
        return redirect(url_for(
                        "profile", username=session["user"]))

    return render_template("addRecipe.html")


@app.route("/editRecipe/<recipe_id>", methods=["GET", "POST"])
def editRecipe(recipe_id):
    if request.method == "POST":
        edit = {'$set': {
            "recipe_name": request.form.get("recipe_name").lower(),
            "serves": request.form.get("serves"),
            "cooking_time": request.form.get("cooktime"),
            "image_url": request.form.get("image_url"),
            "ingredient_name": request.form.getlist("ingredient_name"),
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
    # name = n
    # quantity = q
    # unit = u
    menu_recipes = recipes.find({"is_menu": session["user"]})
    menu_ingredient_ns = []
    menu_ingredient_qs = []
    menu_ingredient_us = []

    for recipe in menu_recipes:
        recipe_ingredient_ns = recipe["ingredient_name"]
        recipe_ingredient_qs = recipe["ingredient_quantity"]
        recipe_ingredient_us = recipe["ingredient_unit"]
        i = 0
        imax = len(recipe_ingredient_ns) - 1

        while i <= imax:
            recipe_ingredient_n = recipe_ingredient_ns[i]
            recipe_ingredient_q = recipe_ingredient_qs[i]
            recipe_ingredient_u = recipe_ingredient_us[i]

            if recipe_ingredient_n in menu_ingredient_ns:
                # Find index of matching ingredient name
                index = menu_ingredient_ns.index(recipe_ingredient_n)
                quantityOne = int(menu_ingredient_qs[index])
                quantityTwo = int(recipe_ingredient_qs[i])
                unitOne = menu_ingredient_us[index]
                unitTwo = recipe_ingredient_us[i]
                # Add the quantity of ingredient i to ingredient index
                if unitOne == unitTwo:
                    menu_ingredient_qs[index] = quantityOne + quantityTwo
                else:
                    menu_ingredient_ns.append(recipe_ingredient_n)
                    menu_ingredient_qs.append(recipe_ingredient_q)
                    menu_ingredient_us.append(recipe_ingredient_u)
                i += 1
            else:
                menu_ingredient_ns.append(recipe_ingredient_n)
                menu_ingredient_qs.append(recipe_ingredient_q)
                menu_ingredient_us.append(recipe_ingredient_u)
                i += 1

            # if recipe_ingredient_name in menu_ingredient_ns:
            #     index = menu_ingredient_ns.index(recipe_ingredient_name)
            #     print(recipe_ingredient_qs)
            #     print(recipe_ingredient_qs[i])
            #     i += 1
            # else:
            #     menu_ingredient_ns.append(recipe_ingredient_name)
            #     menu_ingredient_qs.append(recipe_ingredient_quantity)
            #     menu_ingredient_us.append(recipe_ingredient_unit)
            #     i += 1

        print(menu_ingredient_ns)
        print(menu_ingredient_qs)
        print(menu_ingredient_us)

    # for recipe in menu_recipes:
    #     menu_ingredient_names.extend(recipe["ingredient_name"])
    #     menu_ing_quantities.extend(recipe["ingredient_quantity"])
    #     menu_ingredient_units.extend(recipe["ingredient_unit"])

    # menu_ingredients = [menu_ingredient_names,
    #                     menu_ingredient_quantities,
    #                     menu_ingredient_units]
    # print(menu_ingredient_names)
    # print(menu_ingredient_quantities)
    # print(menu_ingredient_units)
    # print(menu_ingredients)

    # # row[0] is ingredient name
    # print(menu_ingredients[0][0])
    # # row[1] is ingredient quantity
    # print(menu_ingredients[1][0])
    # # row[2] is ingredient unit
    # print(menu_ingredients[2][0])
    # print(len(menu_ingredients[0]))

    # if ingredients name

        # if ingredient is already in 

        # ingredient_quantity = recipe["ingredient_quantity"]
        # ingredient_unit = recipe["ingredient_unit"]
        # for ingredients in ingredient_name:
        #     if ingredients in ingredient_names:
        #         pass
        #     else:
        #         ingredient_names.append(ingredients)
        # print(ingredient_names)
        # print(len(ingredient_name))

    # for recipe in menu_recipes:
    #     ingredient_names += recipe["ingredient_name"]
    #     ingredient_quantities += recipe["ingredient_quantity"]
    #     ingredient_units += recipe["ingredient_unit"]

    # menu_ingredients = zip(ingredient_names,
    #                        ingredient_quantities,
    #                        ingredient_units)

    # menu_recipes = recipes.find({"is_menu": session["user"]})
    # return render_template(
    #     "menu.html", menu_recipes=menu_recipes,
    #     menu_ingredients=menu_ingredients)

    menu_recipes = recipes.find({"is_menu": session["user"]})
    return render_template(
        "menu.html", menu_recipes=menu_recipes)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to false when submitting
            debug=True)
