import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Category, Genre, Title


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/titles.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file, open(
            f'{settings.DATA_IMPORT_LOCATION}/genre_title.csv',
            'r',
            encoding='utf-8-sig',
        ) as genre_file:
            csv_file = csv.reader(csv_file)
            genre_file = csv.reader(genre_file)
            next(csv_file)
            next(genre_file)
            genre_file = list(genre_file)
            genre_line = 1

            for counter, line in enumerate(csv_file):
                name = line[1]
                year = line[2]
                category = Category.objects.get(id=line[3])

                if not Title.objects.filter(
                    name=name,
                    year=year,
                    category=category,
                ).exists():
                    obj = Title()
                    obj.name = name
                    obj.year = year
                    obj.category = category
                    obj.save()
                    for counter1, line1 in enumerate(
                        genre_file[genre_line - 1:],  # fmt: skip
                    ):
                        if int(line1[1]) > counter:
                            break
                        obj.genre.add(Genre.objects.get(id=line1[2]))
                        genre_line += 1
                    print(obj)

            print(f'Import complete, imported {counter} products')
