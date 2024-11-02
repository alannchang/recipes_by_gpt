from flask import Flask, render_template, request
from prompt import prompt
from contextlib import contextmanager

app = Flask(__name__)

blog_recipes = [
    {
        "id": 1,
        "title": "First Recipe",
        "contents": {
            "ingredients_title": "Ingredients",
            "ingredients": "Sample ingredients list",
            "instructions_title": "Instructions",
            "instructions": "Sample cooking instructions",
            "tips_title": "Tips",
            "tips": "Sample cooking tips",
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
    # response = prompt(query)
    response = {
        "title": query,
        "contents": {
            "ingredients_title": "Ingredients",
            "instructions_title": "Instructions",
            "tips_title": "Tips",
            "ingredients": "list of ingredients",
            "instructions": "list of instructions",
            "tips": "list of tips",
        },
    }
    blog_recipes.append(
        {
            "id": len(blog_recipes) + 1,
            "title": query,
            "contents": response["contents"],
        }
    )
    return render_template(
        "recipe.html", recipes=blog_recipes, selected_recipe=response
    )


if __name__ == "__main__":
    app.run(debug=True)
