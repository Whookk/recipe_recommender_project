# routes.py
from flask import request, jsonify
from models import db, RecipeIngredient, Ingredient, Recipe, Cuisine
from sqlalchemy.orm import joinedload
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import aliased
#from flask_jwt_extended import create_access_token, jwt_required, JWTManager


def register_routes(app):
    @app.route('/api/recommendations', methods=['POST'])
    def get_recommendations():
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        print(ingredients)
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400

       
        subquery = (
    RecipeIngredient.query
    .join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.ingredient_id)
    .filter(or_(*[Ingredient.ingredient_name.ilike(f"%{ingredient}%") for ingredient in ingredients]))  
    .with_entities(RecipeIngredient.recipe_id, func.count(Ingredient.ingredient_id).label("match_count"))
    .group_by(RecipeIngredient.recipe_id)
    .subquery()
)

# Основний запит для вибору рецептів
        recipes = (
    Recipe.query
    .join(subquery, Recipe.recipe_id == subquery.c.recipe_id)
    .filter(subquery.c.match_count == len(ingredients))  # Перевіряємо, чи всі інгредієнти є в рецепті
    .options(joinedload(Recipe.ingredients))  # Завантажуємо всі інгредієнти для кожного рецепту
    .all()
)

        if not recipes:
            return jsonify({"message": "No recipes found for the provided ingredients"}), 404
        
        

        response = []
        for recipe in recipes:
          response.append({
          "recipe_id": str(recipe.recipe_id),
          "recipe_name": recipe.recipe_name,
          "instructions": recipe.instructions,
          "cuisine": recipe.cuisine.cuisine_name if recipe.cuisine else None,
          "dietary_info": recipe.dietary_info,
          "cooking_time": recipe.cooking_time,
          "ingredients": [ingredient.ingredient_name for ingredient in recipe.ingredients],
    })

        return jsonify(response), 200
