from django.urls import path

from .views import CreateUserAPIView
from .views import FollowUser, GetFollowersList
from .views import JWTView
from .views import GetPublicKeyView, CheckAccess
from .views import UserSearch
from .views import CreatePitt

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('auth/', JWTView.as_view()),
    path('secret_key/', GetPublicKeyView.as_view()),
    path('authorize/', CheckAccess.as_view()),
    path('subscribe/<slug:me>/<slug:pk>/', FollowUser.as_view()),
    path('list/<slug:person>', GetFollowersList.as_view()),
    path('search/<slug:person>', UserSearch.as_view()),
    path('create_pitt/', CreatePitt.as_view())

]
s