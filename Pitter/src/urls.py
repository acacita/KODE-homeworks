from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('base/', include('api.urls')),
]
