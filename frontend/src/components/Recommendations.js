import React, { useState } from "react";
import axios from "axios";

const Recommendations = () => {
    // Стан для збереження даних
    const [selectedIngredients, setSelectedIngredients] = useState([]);
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // Функція отримання рекомендацій
    const fetchRecommendations = async () => {
        setLoading(true);
        setError("");
        try {
            const response = await axios.post("http://127.0.0.1:5000/api/recommendations", {
                ingredients: selectedIngredients,
            });
            setRecipes(response.data); // Зберігаємо список рецептів
        } catch (err) {
            if (err.response) {
                setError(err.response.data.message); // Виведення повідомлення від сервера
            } else {
                setError("An error occurred while fetching recommendations.");
            }
        } finally {
            setLoading(false);
        }
    };

    // Функція відображення рецептів
    const renderRecipes = () => {
        if (loading) {
            return <p>Loading recommendations...</p>;
        }

        if (error) {
            return <p>{error}</p>;
        }

        if (recipes.length === 0) {
            return <p>No recommendations available.</p>;
        }

        return (
            <div>
                <h2>Recommended Recipes</h2>
                <ul>
                    {recipes.map((recipe) => (
                        <li key={recipe.recipe_id}>
                            <h3>{recipe.recipe_name}</h3>
                            <p><strong>Cuisine:</strong> {recipe.cuisine || "N/A"}</p>
                            <p><strong>Dietary Info:</strong> {recipe.dietary_info || "N/A"}</p>
                            <p><strong>Cooking Time:</strong> {recipe.cooking_time} minutes</p>
                            <p><strong>Ingredients:</strong> {recipe.ingredients.join(", ")}</p>
                            <p><strong>Instructions:</strong> {recipe.instructions}</p>
                        </li>
                    ))}
                </ul>
            </div>
        );
    };

    // Функція для додавання інгредієнтів
    const handleAddIngredient = (ingredient) => {
        if (!selectedIngredients.includes(ingredient)) {
            setSelectedIngredients([...selectedIngredients, ingredient]);
        }
    };

    return (
        <div>
            <h1>Recipe Recommender</h1>
            {/* Ввід інгредієнтів */}
            <div>
                <input
                    type="text"
                    placeholder="Enter an ingredient"
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && e.target.value.trim() !== "") {
                            handleAddIngredient(e.target.value.trim());
                            e.target.value = "";
                        }
                    }}
                />
                <ul>
                    {selectedIngredients.map((ingredient, index) => (
                        <li key={index}>{ingredient}</li>
                    ))}
                </ul>
            </div>
            <button onClick={fetchRecommendations}>Get Recommendations</button>
            {/* Відображення результатів */}
            {renderRecipes()}
        </div>
    );
};

export default Recommendations;
