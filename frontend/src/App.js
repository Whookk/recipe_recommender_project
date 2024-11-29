// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
//import IngredientInput from './components/IngredientInput';
import RecipeList from './components/RecipeList';
import './components/App.css'; 

function App() {
    const [ingredients, setIngredients] = useState([]);
    const [recipes, setRecipes] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const addIngredient = (ingredient) => {
        setIngredients([...ingredients, ingredient]);
    };

    const removeIngredient = (indexToRemove) => {
        setIngredients(ingredients.filter((_, index) => index !== indexToRemove));
    };

    const getRecommendations = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post("http://localhost:5000/api/recommendations", { ingredients });
            if (response.data.length === 0) {
                setError('No recommendations found for the selected ingredients.');
            } else {
                setRecipes(response.data);
            }
        } catch (error) {
            console.error("Error fetching recommendations:", error);
            setError('There are no recipes found whith provided ingredients.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <h1 className="main-title">Recipe Recommender</h1>
            
            {/* Ingredient input form */}
            <div className="input-container">
                <input 
                    className="ingredient-input"
                    type="text" 
                    placeholder="Enter ingredient" 
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            addIngredient(e.target.value);
                            e.target.value = ''; // clear input after adding
                        }
                    }} 
                />
                <button className="recommend-button" onClick={getRecommendations}>
                    Get Recommendations
                </button>
            </div>
            
            {/* Selected ingredients */}
            {ingredients.length > 0 && (
                <div className="selected-ingredients">
                    <h3 className="section-title">Selected Ingredients</h3>
                    <ul>
                        {ingredients.map((ingredient, index) => (
                            <li key={index}>
                                {ingredient} 
                                <button className="remove-button" onClick={() => removeIngredient(index)}>×</button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Loading state */}
            {loading && <p>Loading...</p>}

            {/* Error state */}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {/* Display recipes */}
            {recipes.length > 0 && (
                <div>
                    <h2 className="section-title">Recommended Recipes</h2>
                    <RecipeList recipes={recipes} />
                </div>
            )}
        </div>
    );
}

export default App;