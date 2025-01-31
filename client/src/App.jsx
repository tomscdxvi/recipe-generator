import { useEffect, useState } from 'react'
import './App.css'
import Recipes from './components/recipes';
import RecipeGenerator from './components/prompt';

function App() {

    const [recipes, setRecipes] = useState([]);

    const fetchRecipes = async () => {

        const response = await fetch("http://127.0.0.1:5000/recipes");
        const data = await response.json();

        setRecipes(data.recipes);
        console.log(recipes);
    }

    useEffect(() => {
        fetchRecipes();
    }, []);

    return (
        <>
            <RecipeGenerator />

            <Recipes recipes={recipes} />
        </>
    )
}

export default App
