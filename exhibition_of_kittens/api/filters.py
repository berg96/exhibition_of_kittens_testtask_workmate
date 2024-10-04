import django_filters
from django.db.models import Case, When, Q, Value, IntegerField

from kittens.models import Breed, Kitten


class KittenFilter(django_filters.FilterSet):
    breed = django_filters.ModelMultipleChoiceFilter(
        queryset=Breed.objects.all(), to_field_name='slug',
        field_name='breed__slug'
    )
    breed_name = django_filters.CharFilter(method='filter_breed_name')

    class Meta:
        model = Kitten
        fields = ['breed',]

    def filter_breed_name(self, kittens, name, value):
        return kittens.filter(
            Q(breed__name__icontains=value.lower()) |
            Q(breed__name__istartswith=value.capitalize())
        ).annotate(
            sort_by=Case(
                When(
                    Q(breed__name__istartswith=value.capitalize()),
                    then=Value(1)
                ),
                When(Q(breed__name__icontains=value.lower()), then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('sort_by')
