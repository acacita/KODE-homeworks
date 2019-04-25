from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class UserRetrieveAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=200)


class GetPublicKeyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return Response(
            {'public key': api_settings.JWT_PUBLIC_KEY},
            status=200)
