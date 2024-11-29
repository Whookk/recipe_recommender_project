import uuid
import psycopg2

# Параметри підключення до бази даних
conn = psycopg2.connect(
    dbname="recipes_db",
    user="postgres",
    password="StrongPassword1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Приклади даних для заповнення
recipes = [
    {
        "recipe_name": "Tacos al Pastor",
        "instructions": "1. Marinate pork in a mixture of pineapple juice, chili powder, garlic, and vinegar. 2. Cook the pork on a grill or skillet until caramelized. 3. Serve on warm corn tortillas with diced onions, cilantro, and pineapple.",
        "cuisine": "Mexican",
        "dietary_info": "Non-Vegetarian",
        "cooking_time": 60,
        "ingredients": ["pork", "pineapple juice", "chili powder", "garlic", "vinegar", "corn tortillas", "onions", "cilantro"]
    },
    {
        "recipe_name": "Miso Soup",
        "instructions": "1. Heat water and add dashi granules to create the broth. 2. Mix miso paste into the broth until dissolved. 3. Add tofu cubes and seaweed. 4. Garnish with green onions and serve warm.",
        "cuisine": "Japanese",
        "dietary_info": "Vegetarian",
        "cooking_time": 15,
        "ingredients": ["water", "dashi granules", "miso paste", "tofu", "seaweed", "green onions"]
    },
    {
        "recipe_name": "Fish and Chips",
        "instructions": "1. Coat fish fillets in a batter made of flour, beer, and baking powder. 2. Deep-fry until golden and crispy. 3. Serve with thick-cut fries, lemon wedges, and tartar sauce.",
        "cuisine": "English",
        "dietary_info": "Non-Vegetarian",
        "cooking_time": 30,
        "ingredients": ["fish fillets", "flour", "beer", "baking powder", "potatoes", "lemon", "tartar sauce"]
    },
    {
        "recipe_name": "Ratatouille",
        "instructions": "1. Slice zucchini, eggplant, and bell peppers. 2. Layer vegetables in a baking dish with tomato sauce. 3. Drizzle with olive oil and season with herbs. 4. Bake until tender and fragrant.",
        "cuisine": "French",
        "dietary_info": "Vegan",
        "cooking_time": 50,
        "ingredients": ["zucchini", "eggplant", "bell peppers", "tomato sauce", "olive oil", "herbs"]
    },
    {
        "recipe_name": "Falafel Wrap",
        "instructions": "1. Blend chickpeas, parsley, onion, and spices to form a dough. 2. Shape into balls and fry until golden. 3. Serve in a pita with tahini, lettuce, and tomatoes.",
        "cuisine": "Middle Eastern",
        "dietary_info": "Vegan",
        "cooking_time": 35,
        "ingredients": ["chickpeas", "parsley", "onion", "spices", "pita bread", "tahini", "lettuce", "tomatoes"]
    },
    {
        "recipe_name": "Butter Chicken",
        "instructions": "1. Marinate chicken in yogurt, garlic, and spices. 2. Cook chicken in butter until browned. 3. Add tomato sauce and cream, simmer until thickened. 4. Serve with naan or rice.",
        "cuisine": "Indian",
        "dietary_info": "Non-Vegetarian",
        "cooking_time": 40,
        "ingredients": ["chicken", "yogurt", "garlic", "spices", "butter", "tomato sauce", "cream", "naan"]
    },
    {
        "recipe_name": "Chocolate Lava Cake",
        "instructions": "1. Melt chocolate and butter together. 2. Mix in sugar, eggs, and flour to form a batter. 3. Pour into ramekins and bake until edges are set but center is gooey. 4. Serve with ice cream.",
        "cuisine": "American",
        "dietary_info": "Vegetarian",
        "cooking_time": 20,
        "ingredients": ["chocolate", "butter", "sugar", "eggs", "flour", "ice cream"]
    },
    {
        "recipe_name": "Pho",
        "instructions": "1. Simmer beef bones with star anise, ginger, and onion to make the broth. 2. Add rice noodles, thinly sliced beef, and toppings like bean sprouts and basil. 3. Serve hot with lime wedges.",
        "cuisine": "Vietnamese",
        "dietary_info": "Non-Vegetarian",
        "cooking_time": 120,
        "ingredients": ["beef bones", "star anise", "ginger", "onion", "rice noodles", "beef", "bean sprouts", "basil", "lime"]
    }
]

for recipe in recipes:
    # Додати або отримати cuisine_id
    cursor.execute(
        """
        INSERT INTO cuisine (cuisine_id, cuisine_name)
        VALUES (%s, %s)
        ON CONFLICT (cuisine_name) DO NOTHING
        RETURNING cuisine_id;
        """,
        (str(uuid.uuid4()), recipe["cuisine"])
    )
    cuisine_id = cursor.fetchone()
    if not cuisine_id:
        cursor.execute("SELECT cuisine_id FROM cuisine WHERE cuisine_name = %s", (recipe["cuisine"],))
        cuisine_id = cursor.fetchone()[0]
    else:
        cuisine_id = cuisine_id[0]

    # Додати рецепт
    recipe_id = str(uuid.uuid4())
    cursor.execute(
        """
        INSERT INTO recipes (recipe_id, recipe_name, instructions, cuisine_id, dietary_info, cooking_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (recipe_id, recipe["recipe_name"], recipe["instructions"], cuisine_id, recipe["dietary_info"], recipe["cooking_time"])
    )

    # Додати інгредієнти
    for ingredient in recipe["ingredients"]:
        # Додати або отримати ingredient_id
        cursor.execute(
            """
            INSERT INTO ingredients (ingredient_id, ingredient_name)
            VALUES (%s, %s)
            ON CONFLICT (ingredient_name) DO NOTHING
            RETURNING ingredient_id;
            """,
            (str(uuid.uuid4()), ingredient)
        )
        ingredient_id = cursor.fetchone()
        if not ingredient_id:
            cursor.execute("SELECT ingredient_id FROM ingredients WHERE ingredient_name = %s", (ingredient,))
            ingredient_id = cursor.fetchone()[0]
        else:
            ingredient_id = ingredient_id[0]

        # Додати зв’язок між рецептом і інгредієнтом
        cursor.execute(
            """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (%s, %s)
            """,
            (recipe_id, ingredient_id)
        )

# Підтвердити зміни
conn.commit()
cursor.close()
conn.close()
