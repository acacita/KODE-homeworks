from rest_framework.views import APIView
from rest_framework.response import Response
from models.user_models import User, Subscribers
from models.user_serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
# from ..tasks import send_verification_email


class CreateUserAPIView(APIView):
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
        except Exception as e:
            return Response({"message": "Something went wrong, please check your input"}, status=400)


# todo rewrite this using models fields after I figure out how to authorize people
class FollowUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, me, pk):
        user_id = User.objects.get(username=me)
        follower = User.objects.get(username=pk)
        if user_id == follower:
            raise ValidationError('You can not follow yourself')
        queryset = Subscribers.objects.filter(user_id=user_id, follower_id=follower)
        if queryset.exists():
            raise APIException('Follow relationship already exists')
        else:
            follow = Subscribers.objects.create(user_id=user_id, follower_id=follower)
            follow.save()
            dets = {'message': 'User {} successfully subscribed to user {}'.format(str(me), str(pk))}
            # send_verification_email.delay(me, pk)
            return Response(dets)

    def delete(self, request, me, pk):
        follower = User.objects.get(username=me)
        followed = User.objects.get(username=pk)
        follow = Subscribers.objects.get(user_id=follower, follower_id=followed)
        if follow is not None:
            follow.delete()
            return Response({'message':'You unfollowed {}'.format(pk)}, status=204)
        else:
            raise APIException('Follow relationship does not exists')


class GetFollowersList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, person):
        user = User.objects.get(username=person)
        data = user.get_connections()
        print(data)  # todo serialize this
        return Response(status=200)
