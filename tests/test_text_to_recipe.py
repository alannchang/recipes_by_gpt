import pytest
from app.text_to_recipe import text_to_recipe_dict


@pytest.fixture
def sample_recipe_text():
    return """title: Simple Pasta

contents:

ingredients:
- 500g pasta
- Salt
- Water

instructions:
1. Boil water in a large pot
2. Add salt and pasta
3. Cook for 10 minutes

tips:
- Reserve some pasta water
- Don't overcook"""


@pytest.fixture
def sample_recipe_without_title():
    return """contents:

ingredients:
- Bread
- Butter

instructions:
1. Spread butter on bread

tips:
- Use room temperature butter"""


def test_basic_recipe_parsing():
    recipe_text = """title: Test Recipe
    
contents:

ingredients:
- Ingredient 1
- Ingredient 2

instructions:
1. Step 1
2. Step 2

tips:
- Tip 1"""

    result = text_to_recipe_dict(recipe_text, "Default Title")

    assert result["title"] == "Test Recipe"
    assert len(result["contents"]["ingredients"]) == 2
    assert len(result["contents"]["instructions"]) == 2
    assert len(result["contents"]["tips"]) == 1


def test_recipe_with_default_title(sample_recipe_without_title):
    result = text_to_recipe_dict(sample_recipe_without_title, "Default Recipe")

    assert result["title"] == "Default Recipe"
    assert "Bread" in result["contents"]["ingredients"]
    assert "Butter" in result["contents"]["ingredients"]


def test_recipe_sections(sample_recipe_text):
    result = text_to_recipe_dict(sample_recipe_text, "Default Title")

    assert "ingredients" in result["contents"]
    assert "instructions" in result["contents"]
    assert "tips" in result["contents"]


def test_instruction_number_removal(sample_recipe_text):
    result = text_to_recipe_dict(sample_recipe_text, "Default Title")

    # Check that number prefixes are removed
    assert not any(
        instruction.startswith(tuple("0123456789"))
        for instruction in result["contents"]["instructions"]
    )
    assert "Boil water in a large pot" in result["contents"]["instructions"]


def test_empty_sections():
    recipe_text = """title: Empty Recipe

contents:

ingredients:

instructions:

tips:
"""
    result = text_to_recipe_dict(recipe_text, "Default Title")

    assert result["contents"]["ingredients"] == []
    assert result["contents"]["instructions"] == []
    assert result["contents"]["tips"] == []


def test_malformed_input():
    recipe_text = "Just some random text\nwithout proper formatting"
    result = text_to_recipe_dict(recipe_text, "Default Title")

    assert result["title"] == "Default Title"
    assert all(len(section) == 0 for section in result["contents"].values())
