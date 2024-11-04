// RecipeList.js
import React from 'react';

function RecipeList({ recipes }) {
    return (
        <div>
            {recipes.map((recipe) => (
                <div key={recipe.id}>
                    <h3>{recipe.name}</h3>
                    <p>{recipe.instructions}</p>
                </div>
            ))}
        </div>
    );
}

export default RecipeList;
