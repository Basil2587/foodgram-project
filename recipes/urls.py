from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_recipe/", views.new_recipe, name="new_recipe"),
    path(
        "<username>/<int:recipe_id>/edit/",
        views.recipe_edit,
        name="recipe_edit"
    ),
    path(
        "<username>/<int:recipe_id>/delete/",
        views.recipe_delete,
        name="recipe_delete"
    ),
    path("follow/", views.subscriptions_index, name="subscriptions_index"),
    path("favorite_recipe/", views.favorite_index, name="favorite_index"),
    path("shop_list/", views.shop_list, name="shop_list"),
    path(
        "shop_list/dowload/",
        views.dowload_shop_list,
        name="dowload_shop_list"
    ),
    path(
        "shop_list/<int:recipe_id>/",
        views.delete_recipe,
        name="delete_recipe"
    ),
    path("shop_list/", views.shop_list, name="shop_list"),

    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:recipe_id>/", views.recipe_view, name="recipe"),
]
