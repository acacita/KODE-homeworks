from rest_framework.views import APIView
from rest_framework.response import Response
from models.serializers import UserSerializer
from models.models import User


class CreateUserAPIView(APIView):

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
        except Exception as e:
            return Response({"message": "Something went wrong, please check your input"}, status=400)
