from django.urls import path

from .views.users import CreateUserAPIView, DeleteUserAPIView
from .views.subscribers import FollowUser, GetFollowersList
from .views.obtaintoken import JWTView
from .views.authorize import GetPublicKeyView, UserRetrieveAPIView
from .views.search import UserSearch, UserList
from .views.uploading import CreatePitt
from .views.feed import UsersPublicationList, HomePublicationList

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('delete/', DeleteUserAPIView.as_view()),
    path('listall/', UserList.as_view()),
    path('auth/', JWTView.as_view()),
    path('secret_key/', GetPublicKeyView.as_view()),
    path('authorize/', UserRetrieveAPIView.as_view()),
    path('subscribe/<slug:me>/<slug:pk>/', FollowUser.as_view()),
    path('list/<slug:person>', GetFollowersList.as_view()),
    path('search/<slug:person>', UserSearch.as_view()),
    path('create_pitt/', CreatePitt.as_view()),
    path('myfeed/<str:person>', UsersPublicationList.as_view()),
    path('<str:person>/feed', HomePublicationList.as_view())
]
