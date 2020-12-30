def get_ingredients_from_js(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if "nameIngredient" in key:
            _ = key.split("_")
            ingredients[ingredient_name] = int(request.POST[f"valueIngredient_{_[1]}"]) # noqa
    return ingredients
