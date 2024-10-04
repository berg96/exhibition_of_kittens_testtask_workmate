from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Kitten, Breed, Score


@admin.register(Kitten)
class KittenAdmin(admin.ModelAdmin):
    list_display = (
        'display_image', 'name', 'age', 'display_color', 'owner', 'breed'
    )
    search_fields = ('name', 'owner')
    list_display_links = ('display_image', 'name')

    @admin.display(description='Картинка')
    @mark_safe
    def display_image(self, kitten):
        if kitten.image:
            return (
                f'<img src="{kitten.image.url}" '
                'style="width:50px; height:50px;">'
            )

    @admin.display(description='Цвет')
    @mark_safe
    def display_color(self, kitten):
        return (
            f'<div style="background-color:{kitten.color}; '
            f'width:30px; height:30px;">'
        )


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass
