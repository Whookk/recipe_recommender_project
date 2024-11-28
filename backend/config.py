# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:StrongPassword1@localhost:5432/recipes_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
