from django import forms

from .models import Recipe, RecipeIngre


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
        widgets = {
            "tag": forms.CheckboxSelectMultiple(),
        }


class RecipeIngreeForm(forms.ModelForm):
    class Meta:
        model = RecipeIngre
        fields = ("count",)
