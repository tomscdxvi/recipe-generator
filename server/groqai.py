import os
import json
from groq import Groq
from dotenv import load_dotenv
from models import Recipe
from config import db

# Load API Key 
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def draft_message(content, role='user'):

    return {"role": role, "content": content}

def generate_recipe(prompt):
    
    # Calls Groq AI to generate a recipe based on the given prompt.
    messages = [
        {
            "role": "system", 
            "content": """You are a recipe generator that outputs recipes in a structured JSON format.
                Always return a complete recipe with these fields: 
                name, prep_time, cook_time, ingredients, directions, and nutrition_facts.
                The format should be:
                {
                    "name": "Recipe Name",
                    "prep_time": "Preparation Time",
                    "cook_time": "Cooking Time",
                    "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
                    "directions": ["1.Step 1", "2.Step 2", "3.Step 3"],
                    "nutrition_facts": { "calories": "XX kcal", "protein": "XX g", "fat": "XX g" "carbohydrates": "XX g" }
                }
            """
        },
        draft_message(prompt)
    ]

    chat_completion = client.chat.completions.create(
        temperature=1.0,
        n=1,
        model="mixtral-8x7b-32768",
        max_tokens=10000,
        messages=messages
    )

    # Return AI-generated response
    return chat_completion.choices[0].message.content  

def parse_recipe(response_text):
    try:

        # Convert AI response to dictionary
        recipe_data = json.loads(response_text) 
    except json.JSONDecodeError:

        # Handle invalid JSON responses
        return None  

    # Define default values
    defaults = {
        "name": "Unknown Recipe",
        "prep_time": "Unknown",
        "cook_time": "Unknown",
        "ingredients": "No ingredients provided.",
        "directions": "No directions provided.",
        "nutrition_facts": "No nutrition facts available."
    }

    # Ensure all required fields exist, filling in defaults if needed
    for key, default in defaults.items():
        if key not in recipe_data or not recipe_data[key]:
            recipe_data[key] = default

    return recipe_data


def save_recipe_to_db(recipe_data):

    # Save the parsed recipe to the database and return the saved instance.
    new_recipe = Recipe(
        name=recipe_data["name"],
        prep_time=recipe_data["prep_time"],
        cook_time=recipe_data["cook_time"],
        ingredients=json.dumps(recipe_data["ingredients"]),  # Convert list to JSON string
        directions=json.dumps(recipe_data["directions"]),  # Convert list to JSON string
        nutrition_facts=json.dumps(recipe_data["nutrition_facts"])  # Convert dict to JSON string
    )

    try:
        db.session.add(new_recipe)
        db.session.commit()

         # Return the saved recipe object
        return new_recipe 
    
    except Exception as e:
        db.session.rollback()
        print(f"Error saving recipe: {e}")
        return None



