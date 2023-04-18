# Generated by Django 3.2 on 2023-04-18 18:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.CharField(max_length=1000)),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='date_publication'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.CharField(max_length=1000)),
                (
                    'score',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name='ratings',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='date_publication'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Reviews',
            },
        ),
    ]
