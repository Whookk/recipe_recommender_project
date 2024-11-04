// src/App.js
import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import IngredientInput from './components/IngredientInput';
import RecipeList from './components/RecipeList';

function App() {
    const [ingredients, setIngredients] = useState([]);
    const [recipes, setRecipes] = useState([]);

    const addIngredient = (ingredient) => {
        setIngredients([...ingredients, ingredient]);
    };

    const getRecommendations = async () => {
        try {
            const response = await axios.post("http://localhost:5000/api/recommendations", { ingredients });
            setRecipes(response.data);
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        }
    };

    return (
        <div>
            <h1>Recipe Recommender</h1>
            <IngredientInput onAddIngredient={addIngredient} />
            <button onClick={getRecommendations}>Get Recommendations</button>
            <RecipeList recipes={recipes} />
        </div>
    );
}

export default App;

