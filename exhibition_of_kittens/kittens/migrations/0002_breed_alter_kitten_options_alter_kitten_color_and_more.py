# Generated by Django 4.2.16 on 2024-10-01 00:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kittens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Порода',
                'verbose_name_plural': 'Породы',
            },
        ),
        migrations.AlterModelOptions(
            name='kitten',
            options={'default_related_name': 'kittens', 'verbose_name': 'Котенок', 'verbose_name_plural': 'Котята'},
        ),
        migrations.AlterField(
            model_name='kitten',
            name='color',
            field=models.CharField(max_length=7, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='kittens/images/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='kitten',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Хозяин'),
        ),
        migrations.AddField(
            model_name='kitten',
            name='breed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kittens.breed', verbose_name='Порода'),
            preserve_default=False,
        ),
    ]
