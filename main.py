import requests
from bs4 import BeautifulSoup
import json

# Define a function to scrape a single recipe
def scrape_single_recipe(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract recipe details
    title = soup.select_one('.entry-title').text.strip()
    ingredients = [li.text.strip() for li in soup.select('.wprm-recipe-ingredient')]
    instructions = [step.text.strip() for step in soup.select('.wprm-recipe-instruction-text')]
    nutrition = {
        'calories': soup.select_one('.wprm-nutrition-label-text-nutrition-container-calories').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-calories') else "N/A",
        'protein': soup.select_one('.wprm-nutrition-label-text-nutrition-container-protein').text.strip() if
        soup.select_one('.wprm-nutrition-label-text-nutrition-container-protein') else "N/A",
        'carbohydrates': soup.select_one('.wprm-nutrition-label-text-nutrition-container-carbohydrates').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-carbohydrates') else "N/A",
        'fat': soup.select_one('.wprm-nutrition-label-text-nutrition-container-fat').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-fat') else "N/A"
        ,
        "SaturatedFat": soup.select_one('.wprm-nutrition-label-text-nutrition-container-fat').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-fat') else "N/A",
        "Cholesterol": soup.select_one('.wprm-nutrition-label-text-nutrition-container-cholesterol').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-cholesterol') else "N/A",
        "Sodium": soup.select_one('.wprm-nutrition-label-text-nutrition-container-sodium').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-sodium') else "N/A",
        "Potassium": soup.select_one('.wprm-nutrition-label-text-nutrition-container-potassium').text.strip() if soup.select_one('.wprm-nutrition-label-text-nutrition-container-potassium') else "N/A",
        "Sugar": soup.select_one('.wprm-nutrition-label-text-nutrition-container-sugar').text.strip() if  soup.select_one('.wprm-nutrition-label-text-nutrition-container-sugar') else "N/A"
    }
    
    return {
        'title': title,
        'url': url,
        'ingredients': ingredients,
        'instructions': instructions,
        'nutrition': nutrition
    }

# List of recipe URLs
recipe_urls = [
    "https://ohsnapmacros.com/kale-and-quinoa-salad/",  
    "https://ohsnapmacros.com/whipped-feta-dip/",
    "https://ohsnapmacros.com/marry-me-chicken-pasta/",
    "https://ohsnapmacros.com/garlic-tomato-pasta-sauce/",
    "https://ohsnapmacros.com/rocket-pear-salad/", 
    "https://ohsnapmacros.com/air-fryer-filet-mignon/",
    "https://ohsnapmacros.com/cream-of-mushroom-chicken/",
    "https://ohsnapmacros.com/pumpkin-pasta/",
    "https://ohsnapmacros.com/lasagna-pasta-skillet/",
    "https://ohsnapmacros.com/cottage-cheese-lasagna/",
    "https://ohsnapmacros.com/big-mac-casserole/"
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
