import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/category.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                name = line[1]
                slug = line[2]

                if Category.objects.filter(slug=slug).exists():
                    slug_id = Category.objects.only('id').get(slug=slug).id
                    obj = Category(id=slug_id)
                    obj.name = name
                    obj.save(
                        update_fields=[
                            'name',
                        ],
                    )
                    print(obj)

                else:
                    obj = Category()
                    obj.name = name
                    obj.slug = slug
                    obj.save()
                    print(obj)

            print(f'Import complete, imported {counter} products')
