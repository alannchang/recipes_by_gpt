from flask import Flask, render_template
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)


def init_db():
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """
        )
        # Insert sample data if table is empty
        if not db.execute("SELECT * FROM posts").fetchall():
            db.executemany(
                "INSERT INTO posts (title, content) VALUES (?, ?)",
                [
                    ("First Post", "This is my first blog post"),
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


def get_all_posts():
    with get_db() as db:
        posts = db.execute("SELECT * FROM posts").fetchall()
        return [dict(post) for post in posts]


def get_post(post_id):
    with get_db() as db:
        post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        return dict(post) if post else None


# Initialize the database
init_db()

blog_posts = get_all_posts()


@app.route("/")
def home():
    return render_template("blog.html", posts=blog_posts)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = next((post for post in blog_posts if post["id"] == post_id), None)
    return render_template("blog.html", posts=blog_posts, selected_post=post)


if __name__ == "__main__":
    app.run(debug=True)
