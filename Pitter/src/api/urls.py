from django.urls import path

from .views.users import CreateUserAPIView
from .views.obtaintoken import JWTView
from .views.accsess_views import GetPublicKeyView, CheckAccess

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('auth/', JWTView.as_view()),
    path('get_key/', GetPublicKeyView.as_view()),
    path('authorize/', CheckAccess.as_view())
]
