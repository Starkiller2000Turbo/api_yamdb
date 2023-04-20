import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/genre_title.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                id = line[0]
                title = Title.objects.get(id=line[1])
                genre = Genre.objects.get(id=line[2])

                if not GenreTitle.objects.filter(
                    title=title,
                    genre=genre,
                ).exists():
                    obj = GenreTitle()
                    obj.id = id
                    obj.title = title
                    obj.genre = genre
                    obj.save()
                    print(obj)

            print(f'Import complete, imported {counter} products')
