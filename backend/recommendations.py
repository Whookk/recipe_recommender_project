# recommendations.py
from models import Recipe

def recommend_recipes(ingredients, cuisine=None, dietary=None, cook_time=None):
    query = Recipe.query
    if cuisine:
        query = query.filter_by(cuisine=cuisine)
    if dietary:
        query = query.filter_by(dietary=dietary)
    if cook_time:
        query = query.filter(Recipe.cook_time <= cook_time)
    if ingredients:
        query = query.filter(Recipe.ingredients.contains(",".join(ingredients)))
    return query.all()
