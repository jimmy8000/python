import pickle

# Function to calculate the difficulty of the recipe
def calc_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"

# Function to take recipe details from the user
def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the time needed to cook the recipe: "))
    ingredients = input("Enter the ingredients, separated by a comma: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    return {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}

# Main code to handle file operations
filename = input("Enter the filename you'd like to open: ")
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Starting with an empty list.")
    data = {'recipes_list': [], 'all_ingredients': []}
except Exception as e:
    print(f"An error occurred: {e}")
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    print("File loaded successfully.")
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Function to add ingredients ensuring no duplicates
def add_ingredients(new_ingredients, all_ingredients):
    for ingredient in new_ingredients:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

number_of_recipes = int(input("Enter the number of recipes you want to add: "))
for _ in range(number_of_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)
    add_ingredients(recipe['ingredients'], all_ingredients)

# Update the data dictionary
data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

# Save the updated data to the file
with open(filename, 'wb') as file:
    pickle.dump(data, file)

print("Data saved successfully.")
