from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    RecipeIngre,
    FollowRecipe,
    FollowUser,
    ShoppingList,
    Tag,
)


class RecipeIngreInline(admin.TabularInline):
    model = RecipeIngre
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngreInline,)


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngreInline,)


class TagsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "color",
        "name",
    )
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngre)
admin.site.register(FollowUser)
admin.site.register(FollowRecipe)
admin.site.register(ShoppingList)
