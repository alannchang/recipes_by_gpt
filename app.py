from flask import Flask, render_template, request
from prompt import prompt
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)


def init_db():
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """
        )
        # Insert sample data if table is empty
        if not db.execute("SELECT * FROM recipes").fetchall():
            db.executemany(
                "INSERT INTO recipes (title, content) VALUES (?, ?)",
                [
                    ("First recipe", "This is my first recipe"),
                ],
            )


@contextmanager
def get_db():
    db = sqlite3.connect("blog.db")
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def get_all_recipes():
    with get_db() as db:
        recipes = db.execute("SELECT * FROM recipes").fetchall()
        return [dict(recipe) for recipe in recipes]


def get_recipe(recipe_id):
    with get_db() as db:
        recipe = db.execute(
            "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
        ).fetchone()
        return dict(recipe) if recipe else None


# Initialize the database
init_db()

blog_recipes = get_all_recipes()


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
    response = prompt(query)
    blog_recipes.append(
        {"id": len(blog_recipes) + 1, "title": query, "content": response}
    )
    return render_template(
        "recipe.html", recipes=blog_recipes, selected_recipe=blog_recipes[-1]
    )


if __name__ == "__main__":
    app.run(debug=True)
