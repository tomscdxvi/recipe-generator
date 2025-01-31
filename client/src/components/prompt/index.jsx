import { useState } from "react";

export default function RecipeGenerator() {
  const [prompt, setPrompt] = useState("");
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateRecipe = async () => {
    if (!prompt.trim()) {
      alert("Please enter a prompt.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/generate_recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.message || "Something went wrong");

      setRecipe(data.recipe);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

  return (
    <div>
        <h1 className="text-2xl font-bold mb-4">AI Recipe Generator</h1>
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "12px" }}>
            <textarea
                style={{ width: "25%", padding: "8px", borderRadius: "8px" }}
                rows="3"
                placeholder="Enter a recipe idea..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <button
                style={{ height: "50px", border: "1px solid black"  }}
                onClick={handleGenerateRecipe}
                disabled={loading}
            >
                {loading ? "Generating..." : "Generate Recipe"}
            </button>
        </div>

        {error && <p style={{ color: "red", marginTop: "12px"}}>{error}</p>}

        {recipe && (
            <div className="mt-6 p-4 border rounded">
                <div>
                    <h3>{recipe.name}</h3>
                    <span>{formatDate(recipe.createdAt)}</span>
                </div>
                <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "24px" }}>
                    <h3>Prep Time: {recipe.prepTime}</h3>
                    <h3>Cooking Time: {recipe.cookTime}</h3>
                </div>
                <div>
                    <h3>Ingredients:</h3>
                    {recipe.ingredients.map((ingredient, index) => (
                        <p key={index} style={{ textAlign: "left" }}>
                            {ingredient}
                        </p>
                    ))}
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
        )}
    </div>
  );
}
