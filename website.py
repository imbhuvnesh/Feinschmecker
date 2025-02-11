#!/usr/bin/python3.11

#############################################################################
##                                                                         ##
## Feinschmecker website                                                   ##
##                                                                         ##
## Feinschmecker, 2024-12-20                                               ##
##                                                                         ##
#############################################################################
# Imports

from owlready2 import *

#############################################################################
# Get recipes from filter

onto = get_ontology(
    "https://jaron.sprute.com/uni/actionable-knowledge-representation/feinschmecker/feinschmecker.rdf").load()


def addNutrientFilter(nutrient, filter, header, body):
    header += "?" + nutrient + "_amount "
    body += "?res feinschmecker:has_" + nutrient + " ?" + nutrient + " . \n"
    body += "?" + nutrient + " feinschmecker:amount_of_" + nutrient + " ?" + nutrient + "_amount . \n"
    if nutrient + "_bigger" in filter:
        body += "FILTER (?" + nutrient + "_amount > " + str(filter[nutrient + "_bigger"]) + ") . \n"
    if nutrient + "_smaller" in filter:
        body += "FILTER (?" + nutrient + "_amount < " + str(filter[nutrient + "_smaller"]) + ") . \n"
    return header, body


# Universal filter
def getRequest(filter):
    header = "SELECT ?name ?instructions (GROUP_CONCAT(?ing_name ; separator = \"#\" ) AS ?ingredients) ?vegan ?vegetarian ?type_name ?time_amount ?difficulty_amount "
    body = "{?res rdf:type feinschmecker:Recipe . \n"
    if "vegan" in filter:
        if filter["vegan"]:
            body += "?res feinschmecker:is_vegan true . \n"
        else:
            body += "?res feinschmecker:is_vegan false . \n"
    body += "?res feinschmecker:is_vegan ?vegan . \n"
    if "vegetarian" in filter:
        if filter["vegetarian"]:
            body += "?res feinschmecker:is_vegetarian true . \n"
        else:
            body += "?res feinschmecker:is_vegetarian false . \n"
    body += "?res feinschmecker:is_vegetarian ?vegetarian . \n"

    if "meal_type" in filter:
        body += "?res feinschmecker:is_meal_type ?type . \n"
        body += "?type feinschmecker:has_meal_type_name \"" + filter["meal_type"] + "\" . \n"
        body += "?type feinschmecker:has_meal_type_name ?type_name . \n"
    else:
        body += "OPTIONAL {?res feinschmecker:is_meal_type ?type . \n"
        body += "   ?type feinschmecker:has_meal_type_name ?type_name}. \n"

    body += "?res feinschmecker:requires_time ?time . \n"
    body += "?time feinschmecker:amount_of_time ?time_amount . \n"
    if "time" in filter:
        body += "FILTER (?time_amount < " + str(filter["time"]) + ") . \n"
    body += "?res feinschmecker:has_difficulty ?difficulty . \n"
    body += "?difficulty feinschmecker:has_numeric_difficulty ?difficulty_amount . \n"
    if "difficulty" in filter:
        body += "FILTER (?difficulty_amount = " + str(filter["difficulty"]) + ") . \n"

    header, body = addNutrientFilter("calories", filter, header, body)
    header, body = addNutrientFilter("protein", filter, header, body)
    header, body = addNutrientFilter("fat", filter, header, body)
    header, body = addNutrientFilter("carbohydrates", filter, header, body)

    # Remaining elements for head
    body += "?res feinschmecker:has_recipe_name ?name . \n"
    body += "?res feinschmecker:has_instructions ?instructions . \n"
    body += "?res feinschmecker:has_ingredient ?ing . \n"
    body += "?ing feinschmecker:has_ingredient_with_amount_name ?ing_name . \n"

    body += "}"
    body += "GROUP By ?name ?instructions ?vegan ?vegetarian ?type_name ?time_amount ?difficulty_amount ?calories_amount ?protein_amount ?fat_amount ?carbohydrates_amount"

    recipe_list = list(default_world.sparql(header + body))
    order = ["name", "instructions", "ingredients", "vegan", "vegetarian", "meal_type", "time", "difficulty", "calories", "protein",
             "fat", "carbohydrates"]
    recipe_list_dict = []
    for r in recipe_list:
        tmp = {}
        for i in range(len(order)):
            tmp[order[i]] = r[i]
        tmp["instructions"] = tmp["instructions"].strip("[]\'").split("\', \'")
        for i, step in enumerate(tmp["instructions"]):
            tmp["instructions"][i] = step.lstrip("step ").lstrip("0123456789")
        recipe_list_dict.append(tmp)
    with onto:
        return recipe_list_dict


#############################################################################
# HTML focused methods

def p(indent: int, text: str):
    prefix = ""
    for i in range(indent):
        prefix += "   "
    print(prefix + text)


# Filter examples:
# Every recipe - {}
# Panuozzo sandwich
#   - {"vegan": False, "vegetarian": False, "time": 35, "meal_type":"Lunch", "difficulty": 2, "calories_smaller": 600, "calories_bigger": 500,
#      "protein_smaller": 25, "protein_bigger": 20, "fat_smaller": 30, "fat_bigger": 20, "carbohydrates_smaller": 60,
#      "carbohydrates_bigger": 50}

def getFilter():
    return {}

def main(recipe_list):
    print("Content-Type: text/html")
    print("")
    print("<!DOCTYPE html>")
    print("")
    print("<html>")
    print("<head>")
    print("   <title>Feinschmecker</title>")
    print("   <meta charset=\"utf-8\" />")
    print("   <meta name=\"robots\" content=\"noindex, nofollow\" />")
    print("   <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />")
    print("   <link rel=\"stylesheet\" type=\"text/css\" href=\"https://jaron.sprute.com/CSS/header.css\" />")
    print("   <link rel=\"stylesheet\" type=\"text/css\" href=\"https://jaron.sprute.com/CSS/format.css\" />")
    print("</head>")

    print("<body>")
    print("<p>Hello</p>")
    print("</body>")
    print("</html>")


#############################################################################
# Initial method

if __name__ == '__main__':
    recipe_list = getRequest({})
    main(recipe_list)

#############################################################################