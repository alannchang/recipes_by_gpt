# Recipes by GPT

# Summary

- This is a simple Flask app that uses the ollama API to generate recipes.
- The app takes a user's input, uses the llama 3.2 model to generate a recipe, and displays the recipe on a webpage. The recipe is composed of ingredients, instructions, and tips.
- The recipe is added to the list of recipes on the homepage's sidebar. 

# How to Run

1. Install the required packages: `pip install -r requirements.txt`
2. Start ollama, and run the llama 3.2 model
2. Run the app: `python app.py`
3. Go to `localhost:5000` in your web browser to see the app.

# Things to Improve
- Save the recipes to a database
- Add functionality to edit and delete recipes
- Generate a grocery list from a selection of recipes
- Allow the user to accept or reject the generated recipe and generate a new one
- Improve response time of the ollama API
- If user wants a new recipe, provide suggestions for how to improve the next generated recipe
