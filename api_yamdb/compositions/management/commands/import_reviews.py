import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Comment, Review, Title
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
                title = Title.objects.get(id=line[1])
                text = line[2]
                author = User.objects.get(id=line[3])
                score = line[4]
                pub_date = line[5]

                if not Review.objects.filter(
                    title=title,
                    text=text,
                    author=author,
                    score=score,
                    pub_date=pub_date,
                ).exists():
                    obj = Comment()
                    obj.title = title
                    obj.text = text
                    obj.author = author
                    obj.score = score
                    obj.pub_date = pub_date
                    obj.save()

                    print(obj)

            print(f'Import complete, imported {counter} products')
