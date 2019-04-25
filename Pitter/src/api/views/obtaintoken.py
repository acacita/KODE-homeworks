from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.user_models import User
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.settings import api_settings


class JWTView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Please provide both username and password'})
        try:
            user = User.objects.get(username=username, password=password)
        except ObjectDoesNotExist:
            return Response({'error': 'Can not authenticate user. Please check your credentials'})
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)
        dets = {'token': token}
        return Response(dets, status=200)
