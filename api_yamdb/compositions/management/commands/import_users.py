import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print('Importing data from:', settings.DATA_IMPORT_LOCATION)

        with open(
            f'{settings.DATA_IMPORT_LOCATION}/users.csv',
            'r',
            encoding='utf-8-sig',
        ) as csv_file:
            csv_file = csv.reader(csv_file)
            next(csv_file)

            for counter, line in enumerate(csv_file):
                username = line[1]
                email = line[2]
                role = line[3]
                bio = line[4]
                first_name = line[5]
                last_name = line[6]

                if User.objects.filter(username=username).exists():
                    user_id = User.objects.only('id').get(username=username).id
                    obj = User(id=user_id)
                    obj.email = email
                    obj.role = role
                    obj.bio = bio
                    obj.first_name = first_name
                    obj.last_name = last_name
                    obj.save(
                        update_fields=[
                            'email',
                            'role',
                            'bio',
                            'first_name',
                            'last_name',
                        ],
                    )
                    print(obj)

                else:
                    obj = User()
                    obj.username = username
                    obj.email = email
                    obj.role = role
                    obj.bio = bio
                    obj.first_name = first_name
                    obj.last_name = last_name
                    obj.save()
                    print(obj)

            print(f'Import complete, imported {counter} products')
