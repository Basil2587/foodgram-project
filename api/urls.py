from django.urls import path

from . import views

urlpatterns = [
    path("ingredients/", views.get_ingredients),
    path("subscriptions", views.subscriptions),
    path("subscriptions/<int:author_id>", views.subscriptions_delete),
    path("favorites", views.favorites),
    path("favorites/<int:recipe_id>", views.favorites_delete),
    path("purchases", views.purchases),
    path("purchases/<int:recipe_id>", views.purchases_delete),

]
