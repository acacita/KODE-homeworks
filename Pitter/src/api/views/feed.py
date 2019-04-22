from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models.user_models import User
from ..models.message_serializers import PublicationSerializer
from ..models.message_model import Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# todo authorize

class UsersPublicationList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, person):
        user = User.objects.get(username=person)
        messages = Message.objects.filter(user=user)
        data = PublicationSerializer(messages, many=True)
        return Response(data.data)


class HomePublicationList(APIView):
    # todo add filtering by timestamp
    # todo add dynamic pagination
    permission_classes = (AllowAny,)

    def get(self, request, person):
        user = User.objects.get(username=person)
        followed_users = user.get_connections()
        messages = Message.objects.filter(user__in=followed_users)
        paginator = Paginator(messages, 10)
        page = self.request.GET.get('page')
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)

        data = PublicationSerializer(messages, many=True)
        return Response(data.data)
