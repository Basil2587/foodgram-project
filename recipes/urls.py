from django.urls import path

from . import additional_views, views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "subscriptions/<int:author_id>/",
        views.subscriptions_delete,
        name="subscriptions_delete",
    ),
    path("subscriptions", views.subscriptions, name="subscriptions"),
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
    path("favorites", views.favorites, name="favorites"),
    path("favorite_recipe/", views.favorite_index, name="favorite_index"),
    path(
        "favorites/<int:recipe_id>/",
        views.favorites_delete,
        name="favor_deleiteste"
    ),
    path("purchases", views.purchases, name="purchases"),
    path("shop_list/", views.shop_list, name="shop_list"),
    path(
        "purchases/<int:recipe_id>/",
        views.purchases_delete,
        name="purchases_delete"
    ),
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
