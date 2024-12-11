import requests
from bs4 import BeautifulSoup
import json

from utils import separate_nutrition, get_time, parse_ingredients


def scrape_single_recipe(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract recipe details
    title = soup.select_one('.post-header__title').text.strip()
    author = soup.select_one('.author-link').text.strip()
    cooking_time = soup.select('li.body-copy-small.list-item span time')    
    ingredients = [li.text.strip() for li in soup.select('.ingredients-list__item')]
    instructions = [li.text.strip() for li in soup.select('.method-steps__list-item')]
    nutrition = [li.text.strip() for li in soup.select('.nutrition-list__item')]
    properties = soup.select('span.terms-icons-list__text')
    
    is_vegan = any("Vegan" in item.text for item in properties)
    is_vegetarian = any("Vegetarian" in item.text for item in properties)
    
    return {
        'title': title,
        'source': url,
        'time': get_time(cooking_time),
        'ingredients': parse_ingredients(ingredients),
        'instructions': instructions,
        'nutrients': separate_nutrition(nutrition),
        'author': author,
        'vegan': is_vegan,
        'vegetarian': is_vegetarian
        
    }

# List of recipe URLs
recipe_urls = [
    "https://www.bbcgoodfood.com/recipes/spinach-sweet-potato-lentil-dhal",
    "https://www.bbcgoodfood.com/recipes/poached-eggs-smoked-salmon-and-bubble-squeak",
    "https://www.bbcgoodfood.com/recipes/gluten-free-lemon-drizzle-cake",
    "https://www.bbcgoodfood.com/recipes/mushroom-bhaji",
    "https://www.bbcgoodfood.com/recipes/sweet-potato-coconut-curry",
    "https://www.bbcgoodfood.com/recipes/cola-ham-maple-mustard-glaze",
    "https://www.bbcgoodfood.com/recipes/beef-wellington",
    "https://www.bbcgoodfood.com/recipes/next-level-roast-beef",
    "https://www.bbcgoodfood.com/recipes/nut-loaf",
    "https://www.bbcgoodfood.com/recipes/ultimate-roast-potatoes",
    "https://www.bbcgoodfood.com/recipes/flavour-bomb-roast-turkey-gravy",
    "https://www.bbcgoodfood.com/recipes/shredded-carbonara-sprouts",
    "https://www.bbcgoodfood.com/recipes/ultimate-gratin-dauphinois",
    "https://www.bbcgoodfood.com/recipes/easy-cheesy-leeks",
    "https://www.bbcgoodfood.com/recipes/smoked-salmon-quinoa-dill-lunch-pot",
    "https://www.bbcgoodfood.com/recipes/crunchy-lettuce-salad-wraps-with-sweet-satay-dip",
    "https://www.bbcgoodfood.com/recipes/panuozzo-sandwich"
]

# List to store all recipe data
all_recipes = []

# Loop over URLs and scrape each recipe
for url in recipe_urls:
    try:
        print(f"Scraping recipe: {url}")
        recipe_data = scrape_single_recipe(url)
        all_recipes.append(recipe_data)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Save all recipes to a single JSON file
output_file = 'recipes.json'
with open(output_file, 'w') as f:
    json.dump(all_recipes, f, indent=4)

print(f"All recipes saved to {output_file}")
