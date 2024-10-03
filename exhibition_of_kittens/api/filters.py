import django_filters

from kittens.models import Breed, Kitten


class KittenFilter(django_filters.FilterSet):
    breed = django_filters.ModelMultipleChoiceFilter(
        queryset=Breed.objects.all(), to_field_name='slug',
        field_name='breed__slug'
    )

    class Meta:
        model = Kitten
        fields = ['breed',]
