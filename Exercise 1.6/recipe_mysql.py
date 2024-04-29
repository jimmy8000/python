import mysql.connector

# Create a connection to the MySQL server

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    password='password')

cursor = conn.cursor()

# Create a new database and use it

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

# Create a table to store recipes

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
    )''')

# Create a main menu function to display the options and execute the selected action

def main_menu(conn, cursor):
    choice = ""
    while(choice != "5"):
        print("What do you want to do? Pick one of the following options:")
        print("1. Add a recipe")
        print("2. Search for a recipe")
        print("3. Updata the recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Goodbye!")
            conn.close()

def create_recipe(conn, cursor):
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time of the recipe: "))
    ingredients = input("Enter the ingredients of the recipe, separated by commas: ").split(", ")
    difficulty = calculate_difficulty(cooking_time, ingredients)
    cursor.execute("INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)", (name, ', '.join(ingredients), cooking_time, difficulty))
    conn.commit()
    print("Recipe added successfully")

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "Hard"

def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall() 
    all_ingredients = set()
    for (ingredients,) in results:
        for ingredient in ingredients.split(", "):
            all_ingredients.add(ingredient.strip())
            
    all_ingredients = sorted(all_ingredients)
    
    print("Available ingredients:")
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient}")
    choice = int(input("Enter the number of the ingredient to search for: "))
    search_ingredient = all_ingredients[choice - 1] 
    
    search_pattern = f"%{search_ingredient}%"
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s", (search_pattern,))
    found_recipes = cursor.fetchall()
    
    if found_recipes:
        print(f"Recipes containing {search_ingredient}:")
        for recipe in found_recipes:
            print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} min, Difficulty: {recipe[4]}")
    else:
        print(f"No recipes found containing {search_ingredient}.")

def update_recipe(conn, cursor):
    recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    if recipe:
        print(f"Recipe found: ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} min, Difficulty: {recipe[4]}")
        name = input("Enter the new name of the recipe (leave empty to keep the current name): ")
        cooking_time = input("Enter the new cooking time of the recipe (leave empty to keep the current cooking time): ")
        ingredients = input("Enter the new ingredients of the recipe, separated by commas (leave empty to keep the current ingredients): ")
        difficulty = calculate_difficulty(int(cooking_time) if cooking_time else recipe[3], ingredients.split(", ") if ingredients else recipe[2].split(", "))
        cursor.execute("UPDATE Recipes SET name = %s, ingredients = %s, cooking_time = %s, difficulty = %s WHERE id = %s", (name or recipe[1], ', '.join(ingredients.split(", ")) if ingredients else recipe[2], cooking_time or recipe[3], difficulty, recipe_id))
        conn.commit()
        print("Recipe updated successfully")
    else:
        print("No recipe found with the given ID")

def delete_recipe(conn, cursor):
    recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    if recipe:
        print(f"Recipe found: ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} min, Difficulty: {recipe[4]}")
        confirm = input("Are you sure you want to delete this recipe? (yes/no): ")
        if confirm == "yes":
            cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
            conn.commit()
            print("Recipe deleted successfully")
        else:
            print("Recipe not deleted")
    else:
        print("No recipe found with the given ID")
        
# Calling main_menu function
main_menu(conn, cursor)