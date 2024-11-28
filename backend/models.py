# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
# Ініціалізація SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    dietary_preferences = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cuisine(db.Model):
    __tablename__ = 'cuisine'
    cuisine_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cuisine_name = db.Column(db.String(100), nullable=False)


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_name = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cuisine_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cuisine.cuisine_id'))
    dietary_info = db.Column(db.String(100))
    cooking_time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    ingredients = db.relationship(
        'Ingredient',
        secondary='recipe_ingredients',
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='select'  
    )
    cuisine = db.relationship('Cuisine', backref='recipes')


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingredient_name = db.Column(db.String(100), nullable=False)


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.recipe_id'), primary_key=True)
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
    quantity = db.Column(db.String(50))


class UserSearch(db.Model):
    __tablename__ = 'user_searches'
    search_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    search_query = db.Column(db.String(255), nullable=False)
    search_date = db.Column(db.DateTime, server_default=db.func.now())


class SavedRecipe(db.Model):
    __tablename__ = 'saved_recipes'
    saved_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.recipe_id'), nullable=False)
    saved_at = db.Column(db.DateTime, server_default=db.func.now())


class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.recipe_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    feedback_date = db.Column(db.DateTime, server_default=db.func.now())


class Session(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    session_start = db.Column(db.DateTime, server_default=db.func.now())
    session_end = db.Column(db.DateTime)