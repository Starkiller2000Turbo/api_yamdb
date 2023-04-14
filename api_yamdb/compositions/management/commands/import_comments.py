import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Comment, Review
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/comments.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                review = Review.objects.get(id=line[1])
                text = line[2]
                author = User.objects.get(id=line[3])
                pub_date = line[4]

                if not Comment.objects.filter(
                    review=review,
                    text=text,
                    author=author,
                    pub_date=pub_date,
                ).exists():
                    obj = Comment()
                    obj.review = review
                    obj.text = text
                    obj.author = author
                    obj.pub_date = pub_date
                    obj.save()

                    print(obj)

            print(f'Import complete, imported {counter} products')
