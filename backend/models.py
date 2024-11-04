# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)  # Stored as comma-separated string
    cuisine = db.Column(db.String)
    dietary = db.Column(db.String)
    cook_time = db.Column(db.Integer)  # Time in minutes
    instructions = db.Column(db.Text)
    favorite = db.Column(db.Boolean, default=False)
