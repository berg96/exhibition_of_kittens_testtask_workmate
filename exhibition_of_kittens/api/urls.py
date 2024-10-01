from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
# router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
