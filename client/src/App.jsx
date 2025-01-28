import { useState } from 'react'
import './App.css'

function App() {

  const [recipes, setRecipes] = useState([]);

  const fetchRecipes = async () => {

    const response = await fetch("http://127.0.0.1:5000/recipes");
    const data = await response.json();

    setRecipes(data.recipes);
    console.log(recipes);
  }

  return (
    <>
      <button onClick={fetchRecipes}>click me</button>
    </>
  )
}

export default App
