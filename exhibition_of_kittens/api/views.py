from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from kittens.models import Breed, Kitten, Score

from .filters import KittenFilter
from .permissions import OwnerOrReadOnly
from .serializers import (
    BreedSerializes, KittenReadSerializer, KittenWriteSerializer,
    ScoreSerializer
)

SCORE_ALREADY = 'Оценка уже поставлена.'
SCORE_REQUIRED = 'Поле score является обязательным.'


class KittenViewSet(ModelViewSet):
    queryset = Kitten.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = KittenFilter
    permission_classes = [OwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return KittenReadSerializer
        return KittenWriteSerializer

    def get_queryset(self):
        return Kitten.objects.annotate(
            rating=Avg('scores__score')
        ).order_by('-rating')

    @action(
        detail=True, methods=['post', 'delete'], url_path='score',
        url_name='score', permission_classes=[IsAuthenticated]
    )
    def set_score(self, request, pk):
        kitten = get_object_or_404(Kitten, pk=pk)
        user = request.user
        if request.method == 'DELETE':
            get_object_or_404(Score, user=user, kitten=kitten).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            if Score.objects.filter(user=user, kitten=kitten).exists():
                raise ValidationError({'errors': SCORE_ALREADY})
            score = Score.objects.create(
                user=user,
                kitten=kitten,
                score=serializer.validated_data['score']
            )
            score.save()
            return Response(
                KittenReadSerializer(kitten).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializes
    http_method_names = ['get']
