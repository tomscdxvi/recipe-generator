from flask import request, jsonify
from config import app, db
from models import Recipe

@app.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
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

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)