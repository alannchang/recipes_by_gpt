def text_to_recipe_dict(text):
    # Initialize dictionary structure
    recipe = {
        "title": "",
        "contents": {"ingredients": [], "instructions": [], "tips": []},
    }

    # Split text into lines and process
    lines = text.strip().split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract title
        if line.startswith("title:"):
            recipe["title"] = line.replace("title:", "").strip()
        # Identify sections
        elif line == "contents:":
            continue
        elif line == "ingredients:":
            current_section = "ingredients"
        elif line == "instructions:":
            current_section = "instructions"
        elif line == "tips:":
            current_section = "tips"
        # Add content to appropriate section
        elif line.startswith("-") and current_section:
            recipe["contents"][current_section].append(line.replace("-", "").strip())
        elif line.startswith(tuple("0123456789")) and current_section:
            # Remove number prefix from instructions
            recipe["contents"][current_section].append(
                line.split(".", 1)[1].strip() if "." in line else line
            )
        elif current_section and line:
            recipe["contents"][current_section].append(line)

    return recipe


# Example text
recipe_text = """Title: Classic Homemade Pizza Recipe

Contents:

Ingredients:
- 2 cups of warm water
- 1 tablespoon of sugar
- 1 teaspoon of active dry yeast
- 3 tablespoons of olive oil
- 1 teaspoon of salt
- 4 cups of all-purpose flour
- 1 cup of pizza sauce (homemade or store-bought)
- 2 cups of shredded mozzarella cheese
- Toppings of choice (e.g. pepperoni, mushrooms, bell peppers, onions)

Instructions:
1. In a large mixing bowl, combine the warm water, sugar, and yeast. Let it sit for 5-10 minutes until the mixture becomes frothy.
2. Add the olive oil, salt, and 2 cups of flour to the bowl. Mix until a shaggy dough forms.
3. Gradually add the remaining 2 cups of flour, kneading the dough for 5-10 minutes until it becomes smooth and elastic.
4. Place the dough in a greased bowl, cover it with plastic wrap, and let it rise in a warm place for 1-2 hours until it has doubled in size.
5. Preheat the oven to 450°F (230°C).
6. Punch down the dough and roll it out into a circle or rectangle shape, depending on your preference.
7. Transfer the dough to a greased pizza pan or baking sheet.
8. Spread the pizza sauce over the dough, leaving a small border around the edges.
9. Sprinkle the shredded mozzarella cheese over the sauce.
10. Add your desired toppings and bake for 15-20 minutes until the crust is golden brown and the cheese is melted.

Tips:
- Make sure to knead the dough long enough to develop its gluten, which will give it a better texture.
- Let the dough rise in a warm place, such as near a radiator or oven.
- Use a pizza stone in the oven to achieve a crispy crust.
- Don't overload the pizza with toppings, as this can make the crust soggy.
- Consider using a pizza peel or parchment paper to transfer the dough to the oven."""

if __name__ == "__main__":
    recipe = text_to_recipe_dict(recipe_text)
    # print(recipe)
    print(recipe["Contents"]["Tips"])
