import pytest
from app import app
from app.routes import blog_recipes
from app.text_to_recipe import text_to_recipe_dict
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"First Recipe" in response.data


def test_recipe_route_existing(client):
    response = client.get("/recipe/1")
    assert response.status_code == 200
    assert b"First Recipe" in response.data
    assert b"Sample ingredients list" in response.data


def test_recipe_route_nonexistent(client):
    response = client.get("/recipe/999")
    assert response.status_code == 404
    assert b"Recipe Not Found" in response.data


# Decorators are used to mock the prompt and text_to_recipe_dict functions
@patch("app.routes.prompt")
@patch("app.routes.text_to_recipe_dict")
def test_search_route(mock_text_to_recipe_dict, mock_prompt, client):
    # Mock the response from your AI services
    mock_prompt.return_value = "Mocked AI response"
    mock_text_to_recipe_dict.return_value = {
        "title": "Mocked Recipe",
        "contents": {
            "ingredients": ["Mocked ingredient"],
            "instructions": ["Mocked instruction"],
            "tips": ["Mocked tip"],
        },
    }

    response = client.get("/search-by-dish?q=test+query")
    assert response.status_code == 200
    assert b"Mocked Recipe" in response.data

    # Verify the mocks were called correctly
    mock_prompt.assert_called_once_with("test query", "dish")
    mock_text_to_recipe_dict.assert_called_once()

    # Verify new recipe was added to blog_recipes
    assert len(blog_recipes) > 1
    assert blog_recipes[-1]["title"] == "Mocked Recipe"
