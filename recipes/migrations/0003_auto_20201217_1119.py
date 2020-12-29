# Generated by Django 3.1.4 on 2020-12-17 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20201216_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('title', models.CharField(max_length=45, verbose_name='Название')),# noqa
                ('image', models.ImageField(blank=True, upload_to='recipes/', verbose_name='Картинка')),# noqa
                ('description', models.TextField(verbose_name='Текстовое описание')),# noqa
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='data published')),# noqa
                ('time', models.CharField(max_length=45, verbose_name='Время приготовления')),# noqa
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),# noqa
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('title', models.CharField(choices=[('breakfast', 'Завтрак'), ('lunch', 'Обед'), ('dinner', 'Ужин'), ('salads', 'Салаты'), ('bakery products', 'Выпечка')], max_length=20, verbose_name='Название тэга')),# noqa
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_list', to='recipes.recipe', verbose_name='Список покупок')),# noqa
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_list', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),# noqa
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('count', models.FloatField()),# noqa
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингридиент')),# noqa
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепты')),# noqa
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngre', to='recipes.Ingredient', verbose_name='Ингредиенты'),# noqa
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='Тэг'),
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),# noqa
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),# noqa
            ],
        ),
        migrations.CreateModel(
            name='FollowRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),# noqa
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_recipe', to='recipes.recipe', verbose_name='Рецепт')),# noqa
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_recipe', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),# noqa
            ],
        ),
    ]