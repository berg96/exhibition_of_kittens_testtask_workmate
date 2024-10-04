from django.urls import include, path
from rest_framework import routers

from .views import BreedViewSet, KittenViewSet

router = routers.DefaultRouter()
router.register('kittens', KittenViewSet, basename='kittens')
router.register('breeds', BreedViewSet, basename='breeds')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
