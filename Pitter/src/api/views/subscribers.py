from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.user_models import User, Subscribers
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
from ..templates.tasks import post_subscription_email
from django.core.exceptions import ObjectDoesNotExist


class FollowUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            me = request.user
            my_username = me.username
            follower = User.objects.get(username=pk)
            if my_username == pk:
                raise ValidationError('You can not follow yourself')

            queryset = Subscribers.objects.filter(user_id=me, follower_id=follower)
            if queryset.exists():
                raise APIException('Follow relationship already exists')
            else:
                follow = Subscribers.objects.create(user_id=me, follower_id=follower)
                follow.save()
                post_subscription_email.delay(str(me), str(pk))
                dets = {'message': 'User {} successfully subscribed to user {}'.format(str(me), str(pk))}
                return Response(dets)
        except User.DoesNotExist:
            return Response({'message': 'User or follower does not exist'}, status=400)

    def delete(self, request, pk):
        follower = request.user
        followed = User.objects.get(username=pk)
        try:
            follow = Subscribers.objects.get(user_id=follower, follower_id=followed)
        except ObjectDoesNotExist:
            return Response({'message': 'Follow relationship does not exist'}, status=400)
        follow.delete()
        return Response({'message': 'You unfollowed {}'.format(pk)}, status=204)


class GetFollowersList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, person):
        try:
            user = User.objects.get(username=person)
        except ObjectDoesNotExist:
            return Response({'error': 'User with this username does not exist'}, status=400)
        followers = user.get_connections()
        if not followers:
            return Response({'message': 'This user follows no one'}, status=200)
        data = UserSerializer(followers, many=True)

        return Response(data.data, status=200)
