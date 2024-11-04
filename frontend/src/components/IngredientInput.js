// IngredientInput.js
import React, { useState } from 'react';

function IngredientInput({ onAddIngredient }) {
    const [ingredient, setIngredient] = useState("");

    const handleAdd = () => {
        onAddIngredient(ingredient);
        setIngredient("");
    };

    return (
        <div>
            <input
                type="text"
                value={ingredient}
                onChange={(e) => setIngredient(e.target.value)}
                placeholder="Enter ingredient"
            />
            <button onClick={handleAdd}>Add Ingredient</button>
        </div>
    );
}

export default IngredientInput;
