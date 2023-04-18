import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from compositions.models import Title
from reviews.models import Review
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/review.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)
            got_first = False
            got_second = False
            for counter, line in enumerate(csv_file):
                if (
                    len(line) >= 6
                    and line[0].isdigit
                    and line[1].isdigit
                    and line[-2].isdigit
                    and line[-3].isdigit
                ):
                    got_first = True
                    got_second = True
                    id = line[0]
                    title = Title.objects.get(id=line[1])
                    text = ''.join(line[2:-3])
                    author = User.objects.get(id=line[-3])
                    score = line[-2]
                    pub_date = line[-1]
                elif len(line) >= 3 and line[0].isdigit and line[1].isdigit:
                    got_first = True
                    id = line[0]
                    title = Title.objects.get(id=line[1])
                    text = ''.join(line[2:])
                elif len(line) >= 4 and line[-2].isdigit and line[-3].isdigit:
                    got_second = True
                    text += ''.join(line[:-3])
                    author = User.objects.get(id=line[-3])
                    score = line[-2]
                    pub_date = line[-1]
                else:
                    text += ''.join(line)

                if (
                    got_first
                    and got_second
                    and not Review.objects.filter(
                        title=title,
                        text=text,
                        author=author,
                        score=score,
                        pub_date=pub_date,
                    ).exists()
                ):
                    obj = Review()
                    obj.id = id
                    obj.title = title
                    obj.text = text
                    obj.author = author
                    obj.score = score
                    obj.pub_date = pub_date
                    obj.save()
                    got_first = False
                    got_second = False
                    print(obj)

            print(f'Import complete, imported {counter} products')
