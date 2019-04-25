from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.message_serializers import ManyPittsSerializer, PublicationSerializer
from ..models.message_model import Pitt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

PITTS_PER_PAGE=10

class UsersPublicationList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist in a database'}, status=400)
        messages = Pitt.objects.filter(user=user)
        paginator = Paginator(messages, PITTS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages=paginator.page(1)
        except EmptyPage:
            messages=paginator.page(paginator.num_pages)
        ser = ManyPittsSerializer(messages, many=True)
        return Response(ser.data)


class HomePublicationList(APIView):
    # todo add filtering by timestamp
    # todo add dynamic pagination
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist in a database'}, status=400)
        followed_users = user.get_connections()
        messages = Pitt.objects.filter(user__in=followed_users)
        paginator = Paginator(messages, PITTS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)

        data = PublicationSerializer(messages, many=True)
        return Response(data.data)
