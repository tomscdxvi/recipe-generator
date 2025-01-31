import React from 'react';

export default function Recipes({ recipes }) {

    function formatDate(dateString) {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }
      
  return (
    <>
        <div style={{ textAlign: "left" }}>

            <h2>Recipes</h2>

            <div>
                {recipes.map((recipe) => (
                    <div key={recipe.id} style={{ width: "100%", margin: "12px auto", padding: "24px", border: "1px solid black", borderRadius: "8px" }}>
                        <div>
                            <h3>{recipe.name}</h3>
                            <span>{formatDate(recipe.createdAt)}</span>
                        </div>
                        <div style={{ display: "flex", justifyContent: "left", alignItems: "center", gap: "8px" }}>
                            <h4>Prep Time:</h4> <span>{recipe.prepTime}</span>
                            <h4>Cooking Time:</h4> <span>{recipe.cookTime}</span>
                        </div>
                        <div>
                            <h3>Ingredients:</h3>
                            <div>
                                {recipe.ingredients.map((ingredient, index) => (
                                    <p key={index} style={{ textAlign: "left" }}>
                                        {ingredient}
                                    </p>
                                ))}
                            </div>
                        </div>
                        <div>
                            <h3>Directions:</h3>
                            {recipe.directions.map((direction, index) => (
                                <p key={index} style={{ textAlign: "left" }}>
                                    {direction}
                                </p>
                            ))}
                        </div>
                        <div>
                            <h3>Nutrition Facts:</h3>
                            <div style={{ textAlign: "left" }}>
                                <p>Calories: {recipe.nutritionFacts.calories}</p>
                                <p>Carbohydrates: {recipe.nutritionFacts.carbohydrates}</p>
                                <p>Fat: {recipe.nutritionFacts.fat}</p>
                                <p>Protein: {recipe.nutritionFacts.protein}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    </>
  );
}
