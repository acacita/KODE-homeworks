from rest_framework.views import APIView
#
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings
#
from rest_framework.authentication import get_authorization_header

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class CheckAccess(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        header = get_authorization_header(request)
        print(header)
        return Response('ok you are authorized (not really)')


class GetPublicKeyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return Response(
            {'public key': api_settings.JWT_PUBLIC_KEY},
            status=200)
