import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/addRecipe")
def addRecipe():
    return render_template("addRecipe.html")


@app.route("/searchRecipe")
def searchRecipe():
    return render_template("searchRecipe.html")


@app.route("/shoppingList")
def shoppingList():
    return render_template("shoppingList.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        # Change to false when submitting
        debug=True)