from rest_framework.views import APIView
from rest_framework.response import Response

from ..models.user_models import User
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist


class CreateUserAPIView(APIView):
    #todo authorize
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data

        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "account was successfully created"}, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        username = request.data['username']
        if username is None:
            return Response(
                {'message': 'No id was specified'})

        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response({"message": "User successfully deleted!"}, status=200)
        except ObjectDoesNotExist:
            return Response({"error": "This user does not exist"}, status=400)


