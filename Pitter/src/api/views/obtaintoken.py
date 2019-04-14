from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from models.app_models import User
from rest_framework_jwt.settings import api_settings


class JWTView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            password = request.data['password']
            username = request.data['username']
            user = User.objects.get(username=username, password=password)
            if user:
                try:
                    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
                    token = api_settings.JWT_ENCODE_HANDLER(payload)
                    dets = {'token': token}
                    return Response(dets, status=200)

                except Exception as e:
                    raise e
            else:
                return Response({
                    'message': 'Can not authenticate user, please check your input'}, status=403)
        except KeyError:
            return Response({'message': 'Please provide email and a password'}, status=403)
