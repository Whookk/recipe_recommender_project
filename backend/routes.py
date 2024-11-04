# routes.py
from flask import Blueprint, request, jsonify
from models import db, Recipe
from recommendations import recommend_recipes

api = Blueprint("api", __name__)

@api.route("/recommendations", methods=["POST"])
def get_recommendations():
    data = request.json
    ingredients = data.get("ingredients")
    cuisine = data.get("cuisine")
    dietary = data.get("dietary")
    cook_time = data.get("cook_time")

    recipes = recommend_recipes(ingredients, cuisine, dietary, cook_time)
    return jsonify([recipe.to_dict() for recipe in recipes])

@api.route("/favorites", methods=["POST"])
def toggle_favorite():
    recipe_id = request.json.get("recipe_id")
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        recipe.favorite = not recipe.favorite
        db.session.commit()
    return jsonify({"success": True})
