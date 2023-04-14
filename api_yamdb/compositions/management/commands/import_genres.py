import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/genre.csv',
            'r',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                name = line[1]
                slug = line[2]

                if Genre.objects.filter(slug=slug).exists():
                    slug_id = Genre.objects.only('id').get(slug=slug).id
                    p = Genre(id=slug_id)
                    p.name = name
                    p.save(
                        update_fields=[
                            'name',
                        ],
                    )
                    print(p)

                else:
                    p = Genre()
                    p.name = name
                    p.slug = slug
                    p.save()
                    print(p)

            print(f'Import complete, imported {counter} products')