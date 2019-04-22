from rest_framework.views import APIView
from rest_framework.response import Response

from ..models.user_models import User
from ..models.subscriber_model import Subscribers
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
from ..templates.tasks import post_subscription_email


# todo rewrite this using models fields after I figure out how to authorize people
class FollowUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, me, pk):
        try:
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
                post_subscription_email.delay(str(me), str(pk))
                dets = {'message': 'User {} successfully subscribed to user {}'.format(str(me), str(pk))}
                return Response(dets)
        except User.DoesNotExist:
            return Response({'message': 'User or follower does not exist'})

    def delete(self, request, me, pk):
        follower = User.objects.get(username=me)
        followed = User.objects.get(username=pk)
        follow = Subscribers.objects.get(user_id=follower, follower_id=followed)
        if follow is not None:
            follow.delete()
            return Response({'message': 'You unfollowed {}'.format(pk)}, status=204)
        else:
            raise APIException('Follow relationship does not exists')


class GetFollowersList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, person):
        user = User.objects.get(username=person)
        followers = user.get_connections()
        data = UserSerializer(followers, many=True)

        return Response(data.data, status=200)
