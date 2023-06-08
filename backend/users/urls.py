"""URL configuration for users app."""
from django.urls import path, include

from rest_framework import routers

from users.views import UserViewSet, get_token

router = routers.SimpleRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)

token = [
    path('login/', get_token, name='token_obtain'),
]

urlpatterns = (
    path('', include(router.urls)),
    path('auth/token/', include(token))
)
