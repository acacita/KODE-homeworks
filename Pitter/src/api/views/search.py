from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from models.user_models import User
from models.user_serializers import UserSerializer


class UserSearch(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, person):
        if not person:
            return Response(
                {'message': 'Please input username.'},
            )

        try:
            user = User.objects.get(username=person)
        except User.DoesNotExist:
            return Response({'message': 'Not found.'}, status= 400)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=200)
