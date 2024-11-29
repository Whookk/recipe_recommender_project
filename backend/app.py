# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Імпортуємо модулі
from config import Config
from models import db
from routes import register_routes

# Ініціалізація додатку
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Підключаємо базу даних
db.init_app(app)


register_routes(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
