from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.user_models import User
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response({"The account was successfully created": serializer.data}, status=200)
        return Response(serializer.errors, status=400)


class DeleteUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        authorized_user = request.user
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Please provide both username and password'})

        try:
            user = User.objects.get(username=username, password=password)
        except ObjectDoesNotExist:
            return Response({'error': 'This user does not exist'}, status=400)

        if user == authorized_user:
            user.delete()
            return Response({'message': "User successfully deleted!"}, status=200)
        else:
            return Response({'message': 'You can`t really delete another user'}, status=400)
