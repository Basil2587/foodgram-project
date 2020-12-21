import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Ingredient


def get_ingredients(request):
    ingredient = request.GET["query"]
    ingredients = list(
        Ingredient.objects.filter(title__icontains=ingredient).values(
            "title", "dimension"
        )
    )
    return JsonResponse(ingredients, safe=False)


def get_ingredients_from_js(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if "nameIngredient" in key:
            _ = key.split("_")
            ingredients[ingredient_name] = int(request.POST[f"valueIngredient_{_[1]}"])
    return ingredients
