import csv
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv import load_dotenv

from kittens.models import Breed, Kitten, Score

User = get_user_model()

load_dotenv()

BREEDS_FILE_PATH = 'data/breeds.csv'
KITTENS_FILE_PATH = 'data/kittens.csv'
SCORES_FILE_PATH = 'data/scores.csv'
SUPERUSER_SUCCESS = 'Суперпользователь {} успешно создан'
SUCCESS = 'Импортировано {} {} из {}'


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create_user(
            username=os.getenv('SUPERUSER_USERNAME'),
            password=os.getenv('SUPERUSER_PASSWORD'),
            is_superuser=True,
            is_staff=True
        )
        self.stdout.write(self.style.SUCCESS(
            SUPERUSER_SUCCESS.format(user.username)
        ))
        with open(BREEDS_FILE_PATH, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            next(reader)
            breeds = [
                Breed(*row)
                for row in reader
            ]
            Breed.objects.bulk_create(breeds)
        self.stdout.write(self.style.SUCCESS(SUCCESS.format(
            len(breeds), 'пород', BREEDS_FILE_PATH
        )))
        with open(KITTENS_FILE_PATH, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            next(reader)
            kittens = [
                Kitten(
                    name=row[0],
                    color=row[1],
                    age=row[2],
                    description=row[3],
                    breed=Breed.objects.get(id=row[4]),
                    owner=user
                )
                for row in reader
            ]
            Kitten.objects.bulk_create(kittens)
        self.stdout.write(self.style.SUCCESS(SUCCESS.format(
            len(kittens), 'котят', KITTENS_FILE_PATH
        )))
        with open(SCORES_FILE_PATH, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            next(reader)
            scores = [
                Score(
                    kitten=Kitten.objects.get(id=row[0]),
                    user=user,
                    score=row[1]
                )
                for row in reader
            ]
            Score.objects.bulk_create(scores)
        self.stdout.write(self.style.SUCCESS(SUCCESS.format(
            len(scores), 'оценок', SCORES_FILE_PATH
        )))
