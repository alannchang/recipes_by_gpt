from app import app
from flask import Flask, render_template, request
from app.prompt import prompt
from app.text_to_recipe import text_to_recipe_dict


blog_recipes = [
    {
        "id": 1,
        "title": "First Recipe",
        "contents": {
            "ingredients": ["Sample ingredients list"],
            "instructions": ["Sample cooking instructions"],
            "tips": ["Sample cooking tips"],
        },
    }
]


@app.route("/")
def home():
    return render_template("recipe.html", recipes=blog_recipes)


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = next(
        (recipe for recipe in blog_recipes if recipe["id"] == recipe_id), None
    )
    if recipe is None:
        return render_template("404.html"), 404
    return render_template("recipe.html", recipes=blog_recipes, selected_recipe=recipe)


def search(type):
    query = request.args.get("q")
    response = text_to_recipe_dict(prompt(query, type), query)

    new_recipe = {
        "id": len(blog_recipes) + 1,
        "title": response["title"],
        "contents": response["contents"],
    }
    blog_recipes.append(new_recipe)
    return render_template(
        "recipe.html", recipes=blog_recipes, selected_recipe=new_recipe
    )


@app.route("/search-by-dish")
def search_by_dish():
    return search("dish")


@app.route("/search-by-ingredient")
def search_by_ingredient():
    return search("ingredient")
