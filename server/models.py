from config import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    prep_time = db.Column(db.String(80), unique=False, nullable=False)
    cook_time = db.Column(db.String(80), unique=False, nullable=False)
    ingredients = db.Column(db.String(80), unique=False, nullable=False)
    directions = db.Column(db.String(80), unique=False, nullable=False)
    nutrition_facts = db.Column(db.String(80), unique=False, nullable=False)

    def to_json(self): 
        return {
            "id": self.id,
            "name": self.name,
            "prepTime": self.prep_time,
            "cookTime": self.cook_time,
            "ingredients": self.ingredients,
            "directions": self.directions,
            "nutritionFacts": self.nutrition_facts
        }
