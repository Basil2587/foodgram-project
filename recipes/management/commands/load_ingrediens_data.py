from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    help = 'Load ingredients data to database'

    def handle(self, *args, **options):
        with open('recipes/fixtures/ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, dimension = row
                Ingredient.objects.get_or_create(title=title, dimension=dimension)