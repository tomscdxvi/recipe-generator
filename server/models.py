from config import db
from datetime import datetime
import json

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    prep_time = db.Column(db.String(80), unique=False, nullable=False)
    cook_time = db.Column(db.String(80), unique=False, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # Use Text to store JSON string
    directions = db.Column(db.Text, nullable=False)   # Use Text to store JSON string
    nutrition_facts = db.Column(db.Text, nullable=False)  # Use Text to store JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "prepTime": self.prep_time,
            "cookTime": self.cook_time,
            "ingredients": json.loads(self.ingredients),  # Convert JSON string back to list
            "directions": json.loads(self.directions), # Convert JSON string back to list
            "nutritionFacts": json.loads(self.nutrition_facts), # Convert JSON string back to list
            "createdAt": self.created_at.isoformat()  # Convert to ISO format for easier readability
        }
