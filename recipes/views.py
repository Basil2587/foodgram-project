from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from .additional_views import get_ingredients_from_js
from .forms import RecipeForm
from .models import (
    FollowUser,
    Ingredient,
    Recipe,
    RecipeIngre,
    ShoppingList,
    Tag,
    User,
)


def index(request):
    tags_values = request.GET.getlist("filters")
    recipe_list = Recipe.objects.order_by("-pub_date").all()

    if tags_values:
        recipe_list = recipe_list.filter(tag__title__in=tags_values).distinct().all() # noqa
    paginator = Paginator(recipe_list, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "index.html",
        {"page": page, "paginator": paginator, "tags": tags},
    )


@login_required
def new_recipe(request):
    tags = Tag.objects.all()
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST or None, files=request.FILES or None) # noqa
        ingredients_req = get_ingredients_from_js(request)
        if not ingredients_req:
            recipe_form.add_error(None, "Добавьте ингредиенты")
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, count in ingredients_req.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ingredient = RecipeIngre(
                    count=count, ingredients=ingredient, recipe=recipe
                )
                recipe_ingredient.save()
            recipe_form.save_m2m()
            return redirect("index")
        recipe_form = RecipeForm()
    else:
        recipe_form = RecipeForm()
    return render(
        request,
        "formRecipe.html",
        {
            "form": recipe_form,
            "tags": tags,
        },
    )


@login_required
def recipe_edit(request, username, recipe_id):
    tags = Tag.objects.all()
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author=profile)
    if request.user != recipe.author:
        return redirect("recipe", username=request.user.username, recipe_id=recipe_id) # noqa
    if request.method == "POST":
        form = RecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )
        ingredients_req = get_ingredients_from_js(request)
        if form.is_valid():
            RecipeIngre.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, count in ingredients_req.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ingredient = RecipeIngre(
                    count=count, ingredients=ingredient, recipe=recipe
                )
                recipe_ingredient.save()
            form.save_m2m()
            return redirect("index")
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    return render(
        request,
        "formChangeRecipe.html",
        {
            "form": form,
            "recipe": recipe,
            "tags": tags,
        },
    )


def profile(request, username):
    person = get_object_or_404(User, username=username)
    count_post = Recipe.objects.filter(author=person).count()
    post_list = (
        Recipe.objects.order_by("-pub_date")
        .filter(author=person)
        .select_related("author")
    )
    paginator = Paginator(post_list, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    author = User.objects.get(username=username)
    if request.user.is_authenticated:
        follow_status = FollowUser.objects.filter(user=request.user).filter(
            author=person
        )
        if not follow_status:
            follow_stat = None
        else:
            follow_stat = True
        return render(
            request,
            "authorRecipe.html",
            {
                "page": page,
                "paginator": paginator,
                "username": username,
                "author": author,
                "count_post": count_post,
                "follow_stat": follow_stat,
            },
        )
    return render(
        request,
        "authorRecipe.html",
        {
            "page": page,
            "paginator": paginator,
            "username": username,
            "author": author,
            "count_post": count_post,
        },
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe.html", {"recipe": recipe})


@login_required
def subscriptions_index(request):
    authors_list = FollowUser.objects.select_related("user", "author").filter(
        user=request.user
    )
    paginator = Paginator(authors_list, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "myFollow.html", {"page": page, "paginator": paginator}) # noqa


@login_required
def favorite_index(request):
    tags_values = request.GET.getlist("filters")
    following_list = Recipe.objects.filter(
        following_recipe__user__id=request.user.id
    ).all()
    if tags_values:
        following_list = (
            following_list.filter(tag__title__in=tags_values).distinct().all()
        )
    paginator = Paginator(following_list, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(
        request, "favorite.html", {"page": page, "paginator": paginator, "tags": tags} # noqa
    )


@login_required
def shop_list(request):
    shopList = Recipe.objects.filter(shop_list__user=request.user)
    return render(request, "shopList.html", {"shopList": shopList})


@login_required
def delete_recipe(request, recipe_id):
    shop_recipe = get_object_or_404(ShoppingList, recipe_id=recipe_id)
    shop_recipe.delete()
    return redirect("shop_list")


@login_required
def dowload_shop_list(request):
    recipe = Recipe.objects.filter(shop_list__user=request.user)
    ingredients = (
        recipe.values("ingredients__title", "ingredients__dimension")
        .annotate(Sum("recipeingre__count"))
        .order_by()
    )
    content = "Список ингридиентов для приготовления выбранных блюд \n"
    for item in ingredients:
        title = item["ingredients__title"]
        count = item["recipeingre__count__sum"]
        dimension = item["ingredients__dimension"]
        content += f"{title} {count} {dimension}" + "\n"
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=shopping-list.txt"
    return response


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect("index")


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
