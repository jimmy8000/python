import pickle

# Function to display a recipe
def display_recipe(recipe):
    print("Name:", recipe['name'])
    print("Cooking time:", recipe['cooking_time'], "minutes")
    print("Ingredients:", ', '.join(recipe['ingredients']))
    print("Difficulty:", recipe['difficulty'])
    print("----------------------------------------------------------------")

# Function to search for an ingredient and display recipes containing it
def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}: {ingredient}")
    try:
        ingredient_searched = int(input("Enter the ingredient number to search: "))
        searched_ingredient = all_ingredients[ingredient_searched]
        print(f"Recipes containing {searched_ingredient}:")
        found = False
        for recipe in data['recipes_list']:
            if searched_ingredient in recipe['ingredients']:
                display_recipe(recipe)
                found = True
        if not found:
            print("No recipes contain this ingredient.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except IndexError:
        print("No ingredient at that index. Please enter a valid number.")

# Main code
filename = input("Enter the filename you'd like to open: ")
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Starting with an empty list.")
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    search_ingredient(data)
