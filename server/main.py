from flask import request, jsonify
from config import app, db
from models import Recipe
from groqai import generate_recipe, parse_recipe, save_recipe_to_db

@app.route("/recipes", methods=["GET"])
def get_recipes():

    # Queries through all recipes in sql database
    recipes = Recipe.query.all()

    # Map through every object and transform it into json using the to_json method in the Recipe class then reorganize it into a List.
    json_recipes = list(map(lambda x: x.to_json(), recipes))

    return jsonify({"recipes": json_recipes})

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    name = request.json.get("name")
    prep_time = request.json.get("prepTime")
    cook_time = request.json.get("cookTime")
    ingredients = request.json.get("ingredients")
    directions = request.json.get("directions")
    nutrition_facts = request.json.get("nutritionFacts")

    # Validation
    if not name or not prep_time or not cook_time or not ingredients or not directions or not nutrition_facts:
        return (
            jsonify({"message": "You must include the name, preparation time, cook time, ingredients, directions, and nutrition facts of the recipe!"}), 400
        )
    
    new_recipe = Recipe(name=name, prep_time=prep_time, cook_time=cook_time, ingredients=ingredients, directions=directions, nutrition_facts=nutrition_facts)

    try:
        db.session.add(new_recipe)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Recipe created!"}), 201

@app.route("/update_recipe/<int:recipe_id>", methods=["PATCH"])
def update_recipe(recipe_id):
    
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({"message": "Recipe not found!"}), 404 #404 Not found
    
    data = request.json
    recipe.name = data.get("firstName", recipe.name)
    recipe.prep_time = data.get("prepTime", recipe.prep_time)
    recipe.cook_time = data.get("cookTime", recipe.cook_time)
    recipe.ingredients = data.get("ingredients", recipe.ingredients)
    recipe.directions = data.get("directions", recipe.directions)
    recipe.nutrition_facts = data.get("nutritionFacts", recipe.nutrition_facts)

    db.session.commit()

    return jsonify({"message": "Recipe has been updated!"}), 200

@app.route("/delete_recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):

    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({"message": "Recipe not found!"}), 404 #404 Not found
    
    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe has been deleted!"}), 200

@app.route("/generate_recipe", methods=["POST"])
def generate_and_store_recipe():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"message": "Prompt is required!"}), 400

    response_text = generate_recipe(prompt)
    recipe_data = parse_recipe(response_text)

    # Ensure all required fields exist in recipe_data
    required_fields = ["name", "prep_time", "cook_time", "ingredients", "directions", "nutrition_facts"]
    missing_fields = [field for field in required_fields if field not in recipe_data or not recipe_data[field]]

    if missing_fields:
        return jsonify({
            "message": f"AI response is missing required fields: {', '.join(missing_fields)}",
            "recipe_data": recipe_data
        }), 500

    saved_recipe = save_recipe_to_db(recipe_data)

    if saved_recipe is None:
        return jsonify({"message": "Failed to save recipe to the database!"}), 500

    return jsonify({"message": "AI-generated recipe saved!", "recipe": saved_recipe.to_json()}), 201


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)