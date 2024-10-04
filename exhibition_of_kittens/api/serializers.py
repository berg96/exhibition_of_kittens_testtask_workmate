from django.db.models import Avg
from djoser.serializers import UserSerializer
from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import UniqueTogetherValidator

from kittens.models import Breed, Kitten


class BreedSerializes(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class KittenReadSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    image = Base64ImageField()
    breed = BreedSerializes()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Kitten
        fields = '__all__'

    def get_rating(self, kitten):
        return kitten.scores.aggregate(avg_score=Avg('score'))['avg_score']


class KittenWriteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False)
    breed = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), required=True
    )

    class Meta:
        model = Kitten
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Kitten.objects.all(),
                fields=('name', 'owner')
            )
        ]

    def to_representation(self, recipe):
        return KittenReadSerializer(recipe).data


class ScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField(required=True, min_value=1, max_value=5)
