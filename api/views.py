import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from recipes.models import (
    FollowRecipe,
    FollowUser,
    Ingredient,
    Recipe,
    ShoppingList,
    User,
)


@login_required
def subscriptions(request):
    author_id = int(json.loads(request.body).get("id"))
    author = get_object_or_404(User, pk=author_id)
    if request.user.id != author_id:
        FollowUser.objects.create(user=request.user, author=author)
        return JsonResponse({"success": "ok"})


@login_required
def subscriptions_delete(request, author_id):
    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, id=author_id)
    follow_user = get_object_or_404(FollowUser, user=user, author=author)
    follow_user.delete()
    return JsonResponse({"success": True})


@login_required
def favorites(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    FollowRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def favorites_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    follow_recipe = get_object_or_404(FollowRecipe, user=user, recipe=recipe)
    follow_recipe.delete()
    return JsonResponse({"success": True})


@login_required
def purchases(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def purchases_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    obj = get_object_or_404(ShoppingList, user=user, recipe=recipe)
    obj.delete()
    return JsonResponse({"success": True})


def get_ingredients(request):
    ingredient = request.GET["query"]
    ingredients = list(
        Ingredient.objects.filter(title__icontains=ingredient).values(
            "title", "dimension"
        )
    )
    return JsonResponse(ingredients, safe=False)
