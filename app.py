from flask import Flask, render_template, request
from prompt import prompt
from text_to_recipe import text_to_recipe_dict
from contextlib import contextmanager

app = Flask(__name__)

blog_recipes = [
    {
        "id": 1,
        "title": "First Recipe",
        "contents": {
            "ingredients_title": "Ingredients",
            "ingredients": ["Sample ingredients list"],
            "instructions_title": "Instructions",
            "instructions": ["Sample cooking instructions"],
            "tips_title": "Tips",
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
    return render_template("recipe.html", recipes=blog_recipes, selected_recipe=recipe)


@app.route("/search")
def search():
    query = request.args.get("q")
    response = text_to_recipe_dict(prompt(query), query)

    new_recipe = {
        "id": len(blog_recipes) + 1,
        "title": response["title"],
        "contents": response["contents"],
    }
    blog_recipes.append(new_recipe)
    return render_template(
        "recipe.html", recipes=blog_recipes, selected_recipe=new_recipe
    )


if __name__ == "__main__":
    app.run(debug=True)
