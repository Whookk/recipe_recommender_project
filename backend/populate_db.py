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
        "recipe_name": "Lasagna",
        "instructions": "1. Cook and drain the ground beef, then stir in the spaghetti sauce and simmer.  2. Combine the cottage cheese, 2 cups of mozzarella, eggs, half of the Parmesan, and seasonings.. 3. Assemble the lasagna according to the detailed recipe. 4. Bake, covered, for 45 minutes. 5. Uncover and continue baking for 10 minutes. ",
        "cuisine": "Italian",
        "dietary_info": "Non-Vegetarian",
        "cooking_time": 90,
        "ingredients": ["beef", "spagetti sauce", "cheese", "egg", "noodles", "water"]
    },
    {
        "recipe_name": "Awesome and Easy Creamy Corn Casserole",
        "instructions": "Simply mix the ingredients until they're well-combined, transfer to a baking dish, and bake until a toothpick inserted into the center comes out clean.",
        "cuisine": "English",
        "dietary_info": "Vegetarian",
        "cooking_time": 55,
        "ingredients": ["canned corn", "cornbread mix", "sour cream", "butter", "egg"]
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
