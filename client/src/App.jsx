import { useEffect, useState } from 'react';
import Lottie from 'lottie-react';
import './App.css';
import Recipes from './components/recipes';
import RecipeGenerator from './components/prompt';

import FoodLoading from '../src/assets/FoodLoading.json';

function App() {

    const [loading, setLoading] = useState(true);
    const [recipes, setRecipes] = useState([]);

    const fetchRecipes = async () => {

        const response = await fetch("http://127.0.0.1:5000/recipes");
        const data = await response.json();

        setTimeout(() => {
            setLoading(false);
        }, 1000)

        setRecipes(data.recipes);
        console.log(recipes);
    }

    useEffect(() => {
        fetchRecipes();
    }, []);

    if(loading) {
        return (
            <div>
                <div>
                    <Lottie animationData={FoodLoading} loop={true} />
                </div>
            </div>
        )
    } else {
        return (
            <>
                <RecipeGenerator />
    
                <Recipes recipes={recipes} />
            </>
        )
    }
}

export default App
