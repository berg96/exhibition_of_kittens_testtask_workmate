from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()

MAX_LENGTH = 200
MAX_LENGTH_COLOR = 7
MIN_VALUE_AGE = 1
VALIDATE_COLOR_ERROR = 'Цвет должен быть в формате HEX-код'


class Kitten(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Имя')
    color = models.CharField(
        max_length=MAX_LENGTH_COLOR,
        validators=[RegexValidator(
            regex=r'^#[a-fA-F0-9]{6}\Z', message=VALIDATE_COLOR_ERROR
        )],
        verbose_name='Цвет'
    )
    age = models.IntegerField(
        validators=[MinValueValidator(MIN_VALUE_AGE)],
        verbose_name='Возраст (полных месяцев)'
    )
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Хозяин'
    )
    image = models.ImageField(
        upload_to='kittens/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Фото'
    )
    breed = models.ForeignKey(
        'Breed', on_delete=models.CASCADE, verbose_name='Порода'
    )

    class Meta:
        verbose_name = 'Котенок'
        verbose_name_plural = 'Котята'
        default_related_name = 'kittens'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'owner'],
                name='unique_name_owner'
            )
        ]

    def __str__(self):
        return (
            f'{self.owner.username}`s {self.name} {self.breed.name} {self.age} '
            f'{self.color} {self.description[:20]}'
        )


class Breed(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH, unique=True, verbose_name='Название'
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH, unique=True, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.slug}) {self.description[:20]}'
