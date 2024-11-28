// RecipeList.js
import React from 'react';
import './RecipeList.css'; 

const RecipeList = ({ recipes }) => {
    return (
        <div className="recipe-container">
            {recipes.map((recipe) => (
                <div className="recipe-card" key={recipe.recipe_id}>
                    <h3 className="recipe-title">{recipe.recipe_name}</h3>
                    <p><strong>Cuisine:</strong> {recipe.cuisine || 'Unknown'}</p>
                    <p><strong>Cooking Time:</strong> {recipe.cooking_time} minutes</p>
                    <p><strong>Dietary Info:</strong> {recipe.dietary_info || 'N/A'}</p>
                    <h4>Ingredients:</h4>
                    <ul>
                        {recipe.ingredients.map((ingredient, index) => (
                            <li key={index}>{ingredient}</li>
                        ))}
                    </ul>
                    <h4>Instructions:</h4>
                    <p>{recipe.instructions}</p>
                </div>
            ))}
        </div>
    );
};

export default RecipeList;