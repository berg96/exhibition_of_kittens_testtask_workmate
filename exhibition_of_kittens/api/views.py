from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import KittenFilter
from .serializers import (
    BreedSerializes, KittenReadSerializer, KittenWriteSerializer
)
from kittens.models import Breed, Kitten


class KittenViewSet(ModelViewSet):
    queryset = Kitten.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = KittenFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return KittenReadSerializer
        return KittenWriteSerializer


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializes
    http_method_names = ['get']
