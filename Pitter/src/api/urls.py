from django.urls import path

from .views.uploadview import UploadView
from .views.users import CreateUserAPIView

urlpatterns = [
    path('transcribe/', UploadView.as_view()),
    path('signin/', CreateUserAPIView.as_view())
]
