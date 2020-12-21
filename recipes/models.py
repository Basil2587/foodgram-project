from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    tag_options = {
        "breakfast": ["orange", "Завтрак"],
        "lunch": ["green", "Обед"],
        "dinner": ["purple", "Ужин"],
        "salads": ["red", "Салаты"],
    }

    TAG_CHOICES = [
        ("breakfast", "Завтрак"),
        ("lunch", "Обед"),
        ("dinner", "Ужин"),
        ("salads", "Салаты"),
    ]
    title = models.CharField(
        max_length=20, choices=TAG_CHOICES, verbose_name="Название тэга"
    )

    def __str__(self):
        return self.title

    @property
    def color(self):
        return self.tag_options[self.title][0]

    @property
    def name(self):
        return self.tag_options[self.title][1]


class Ingredient(models.Model):
    title = models.CharField(max_length=300, verbose_name="Название")
    dimension = models.CharField(max_length=20, verbose_name="Единица измерения")

    def __str__(self):
        return f"{self.title} {self.dimension}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации",
    )
    title = models.CharField(max_length=45, verbose_name="Название")
    image = models.ImageField(
        upload_to="recipes/", blank=True, verbose_name="Картинка"
    )
    description = models.TextField(verbose_name="Текстовое описание")
    pub_date = models.DateTimeField("data published", auto_now_add=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тэг")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngre",
        through_fields=("recipe", "ingredients"),
        verbose_name="Ингредиенты"
    )
    time = models.CharField(max_length=45, verbose_name="Время приготовления")

    def __str__(self):
        return self.title


class RecipeIngre(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепты"
    )
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингридиент"
    )
    count = models.FloatField()

    def __str__(self):
        return f"{self.recipe}"


class FollowUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Пользователь"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор публикации"
    )

    def __str__(self):
        return self.user.username


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_recipe",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="following_recipe",
        verbose_name="Рецепт"
    )

    def __str__(self):
        return f"user - {self.user} recipe - {self.recipe}"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shop_list",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shop_list",
        verbose_name="Список покупок"
    )

    def __str__(self):
        return self.recipe.title
