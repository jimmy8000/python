# Import necessary packages
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Engine setup
engine = create_engine("mysql+pymysql://cf-python:password@localhost/my_database")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def __repr__(self):
        return f"<Recipe( id={self.id} name={self.name}, difficulty={self.difficulty})>"
    
    def __str__(self):
        return (
            "\n"
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            "-------------------------\n"
        )
    
    def calculate_difficulty(self):
        ingredient_list = self.ingredients.split(',')
        num_ingredients = len(ingredient_list)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"
            
    def return_ingredients_as_list(self):
        if self.ingredients is None:
            return []
        return self.ingredients.split(',')
            
Base.metadata.create_all(engine)

def create_recipe():
    # Collecting recipe name
    while True:
        name = input("Enter the recipe name (up to 50 characters): ").lower().capitalize()
        if len(name) > 50:
            print("Name is too long. Please use 50 characters or fewer.")
        elif not name.isalnum() and not all(c.isalnum() or c.isspace() for c in name):
            print("Name should contain only alphanumeric characters and spaces.")
        else:
            break

    # Collecting number of ingredients
    while True:
        num_ingredients = input("How many ingredients are there? ")
        if num_ingredients.isnumeric():
            num_ingredients = int(num_ingredients)
            break
        else:
            print("Please enter a valid number.")

    # Collecting ingredients
    ingredients = []
    for i in range(num_ingredients):
        while True:
            ingredient = input(f"Enter ingredient {i+1}: ").lower().capitalize()
            if not ingredient:
                print("Ingredient cannot be empty.")
            elif len(ingredient) > 255:
                print("Ingredient description is too long. Please limit to 255 characters.")
            else:
                ingredients.append(ingredient)
                break

    # Joining ingredients into a single string
    ingredients_str = ', '.join(ingredients)

    # Collecting cooking time
    while True:
        cooking_time = input("Enter the cooking time in minutes: ")
        if cooking_time.isnumeric():
            cooking_time = int(cooking_time)
            break
        else:
            print("Please enter a valid integer for cooking time.")

    # Creating a new recipe object
    new_recipe = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    new_recipe.calculate_difficulty()
    session.add(new_recipe)
    session.commit()
    print(f"Recipe '{name}' added to database with difficulty {new_recipe.difficulty}.")

def view_all_recipes():
    # Querying the database for all recipes
    recipes = session.query(Recipe).all()
    
    # Check if the list of recipes is empty
    if not recipes:
        print("No recipes found in the database.")\
    
    # Loop through the recipes and print each one
    for recipe in recipes:
        print(recipe)

def search_by_ingredients():
    # Check if there are any entries in the Recipe table
    hasEntry = session.query(Recipe).count()
    if hasEntry == 0:
        print("No recipes found in the database.")
        return
    
    # Retrieve all ingredients from the database
    results = session.query(Recipe.ingredients).all()
    
    # Create a list of all unique ingredients
    all_ingredients = []
    for result in results:
        # Split each result and add unique ingredients to the list
        ingredients_list = result[0].split(', ')
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Display all ingredients with a number next to each
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index + 1}. {ingredient}")

    # Get user input for ingredients to search by
    input_numbers = input("Enter the numbers of the ingredients you'd like to search for, separated by spaces: ")
    
    # Convert input into a list of integers
    try:
        selected_indices = [int(num) for num in input_numbers.split()]
    except ValueError:
        print("Invalid input. Please enter only numbers separated by spaces.")
        return
    
    # Validate selected indices
    if not all(1 <= num <= len(all_ingredients) for num in selected_indices):
        print("One or more selected numbers are out of valid range.")
        return
    
    # Create a list of ingredients to search for
    search_ingredients = [all_ingredients[i - 1] for i in selected_indices]
    
    # Create SQL LIKE conditions for each selected ingredient
    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    
    # Retrieve and display all recipes that match the search conditions
    if conditions:
        search_results = session.query(Recipe).filter(*conditions).all()
        if search_results:
            for recipe in search_results:
                print(recipe)
        else:
            print("No recipes found with the selected ingredients.")
    else:
        print("No ingredients selected for the search.")
        
def edit_recipe():
    # Check if there are any recipes in the database
    hasEntry = session.query(Recipe).count()
    if hasEntry == 0:
        print("No recipes found in the database.")
        return

    # Retrieve the id and name for each recipe from the database
    results = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    for recipe in results:
        print(f"ID: {recipe.id}, Name: {recipe.name}")
        
    # Get user input for which recipe to edit
    recipe_id = input("Enter the ID of the recipe you want to edit: ")
    try:
        recipe_id = int(recipe_id)
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return
    
    # Retrieve the recipe by ID
    recipe_to_edit = session.get(Recipe, recipe_id)
    if recipe_to_edit is None:
        print("Recipe not found.")
        return
    
    # Display the recipe details
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")
    
    # Get user input for which attribute to edit
    choice = input("Enter the number of the attribute you want to edit: ")
    if choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter a valid number.")
        return
    
    # Edit the selected attribute
    if choice == '1':
        new_name = input("Enter the new name: ").lower().capitalize()
        if len(new_name) > 50:
            print("Name too long. Please keep it under 50 characters.")
            return
        recipe_to_edit.name = new_name
    elif choice == '2':
        new_ingredients = input("Enter the new ingredients, separated by a comma and space: ")
        # Split the input string into a list of ingredients
        ingredient_list = new_ingredients.split(', ')
        # Capitalize each ingredient in the list
        capitalized_ingredients = [ingredient.capitalize() for ingredient in ingredient_list]
        # Join the capitalized ingredients back into a single string
        recipe_to_edit.ingredients = ', '.join(capitalized_ingredients)
    elif choice == '3':
        new_cooking_time = input("Enter the new cooking time in minutes: ")
        if not new_cooking_time.isdigit():
            print("Invalid input. Cooking time must be a number.")
            return
        recipe_to_edit.cooking_time = int(new_cooking_time)

    # Recalculate difficulty
    recipe_to_edit.calculate_difficulty()

    # Commit changes to the database
    session.commit()
    print("Recipe updated successfully.")
    
def delete_recipe():
    # Check if there are any recipes in the database
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return
    
    # Retrieve and display the id and name for each recipe from the database
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe in results:
        print(f"ID: {recipe.id}, Name: {recipe.name}")
        
    # Get user input for which recipe to delete by ID
    try:
        recipe_id_to_delete = int(input("Enter the ID of the recipe you want to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return
    
    # Retrieve the recipe by ID
    recipe_to_delete = session.get(Recipe, recipe_id_to_delete)
    if recipe_to_delete is None:
        print("Recipe not found.")
        return
    
    # Confirm deletion
    is_sure = input(f"Are you sure you want to delete the recipe '{recipe_to_delete.name}'? (y/n): ")
    if is_sure.lower() == 'y':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully.")
    else:
        print("Deletion cancelled.")

# Main loop

def main():
    while True:
        print("\nRecipe App")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to quit the application")
        print("\n")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice.lower() == 'quit':
            print("Exiting the Recipe App. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5 or type 'quit' to exit.")
    
    # Close the session and the engine connection properly
    session.close()
    engine.dispose()

if __name__ == "__main__":
    main()