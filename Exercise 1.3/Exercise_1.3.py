recipes_list = []
ingredients_list = []
n = int(input("How many recipes would you like to add?"))

def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the time needed to cook the recipe: "))
    ingredients = input("Enter the ingredients, separated by a comma: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe

for i in range(n):
    recipe = take_recipe()
    
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)
    
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) > 4:
        recipe["difficulty"] = "Intermediate"
    else: recipe["difficulty"] = "Hard"

for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cook time: ", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])
    
ingredients_list.sort()
print("Ingredients List:")
for ingredient in ingredients_list:
    print(ingredient)
    

destination = input("Where would you like to travel to?")
destination_list = ["Hawaii", "Paris", "Bora Bora"]
if destination in destination_list:
    print("Enjoy your stay in! " + destination)
else: print("Oops, that destination is not currently available.")