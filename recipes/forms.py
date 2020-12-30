from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe, RecipeIngre, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            "title",
            "tag",
            "time",
            "description",
            "image",
        )
        ordering = ['- pub_date']
        widgets = {
            "tag": forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)
        for id in known_ids:
            title = self.data.get(f'nameIngredient_{id}'),
            dimension = self.data.get(f'unitsIngredient_{id}')
            ingredient_exists = Ingredient.objects.filter(
                title=title[0],
                dimension=dimension,
            ).exists()
            if not ingredient_exists:
                raise ValidationError('Выберите ингредиент из списка!')


class RecipeIngreeForm(forms.ModelForm):
    class Meta:
        model = RecipeIngre
        fields = ("count",)
