# Generated by Django 4.2.16 on 2024-10-01 01:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kittens', '0002_breed_alter_kitten_options_alter_kitten_color_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='breed',
            options={'ordering': ('name',), 'verbose_name': 'Порода', 'verbose_name_plural': 'Породы'},
        ),
        migrations.AddField(
            model_name='breed',
            name='slug',
            field=models.SlugField(default=1, max_length=200, unique=True, verbose_name='Слаг'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='breed',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Цвет должен быть в формате HEX-код', regex='^#[a-fA-F0-9]{6}\\Z')], verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='kitten',
            constraint=models.UniqueConstraint(fields=('name', 'owner'), name='unique_name_owner'),
        ),
    ]
