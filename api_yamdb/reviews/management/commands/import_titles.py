import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/titles.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                id = line[0]
                name = line[1]
                year = line[2]
                category = Category.objects.get(id=line[3])

                if not Title.objects.filter(
                    name=name,
                    year=year,
                    category=category,
                ).exists():
                    obj = Title()
                    obj.id = id
                    obj.name = name
                    obj.year = year
                    obj.category = category
                    obj.save()
                    print(obj)

            print(f'Import complete, imported {counter} products')
