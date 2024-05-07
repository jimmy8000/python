class Recipe:
    all_ingredients = set() 
    
    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None
        self.update_all_ingredients()
        
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    
    def get_cooking_time(self):
        return self.cooking_time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()
        
    def get_ingredients(self):
        return self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)
            
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def __str__(self):
        self.get_difficulty()
        return (f"Recipe Name: {self.name}\n"
                f"Ingredients: {', '.join(self.ingredients)}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Difficulty: {self.get_difficulty()}")
        
    def recipe_search(data, ingredient):
        recipes = []
        for recipe in data:
            if recipe.search_ingredient(ingredient):
                recipes.append(recipe)
        return recipes
    
tea = Recipe("Tea",["Tea Leaves", "Sugar", "Water"], 5)
tea.add_ingredients("Ice Cubes")
print(tea)

coffee = Recipe("Coffee",["Coffee Powder", "Sugar", "Water"], 5)
coffee.add_ingredients("Milk")
print(coffee)

cake = Recipe("Cake",["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
cake.add_ingredients("Cocoa Powder")
print(cake)

bananaSmoothie = Recipe("Banana Smoothie",["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)
bananaSmoothie.add_ingredients("Cinnamon Powder")
print(bananaSmoothie)

recipes_list = [tea, coffee, cake, bananaSmoothie]
recipes_with_milk = Recipe.recipe_search(recipes_list, "Milk")
for recipe in recipes_with_milk:
    print(recipe)

