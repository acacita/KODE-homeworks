from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from ..models.message_model import Pitt
from ..models.message_serializers import PublicationSerializer
from ..models.user_serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from ..templates.tasks import send_pitt_notification


class CreatePitt(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        up_file = request.data.get('file', None)
        file_type = str(up_file).split('.')[-1]
        if not up_file:
            return Response({'message': 'the file is missing'}, status=400)

        elif file_type != 'flac':
            return Response({'message': 'Please send only flac files'}, status=406)

        try:
            user = request.user
            my_name = user.username
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist in a database'}, status=400)

        text_content = request.data.get('text_content', None)

        if up_file and file_type == 'flac':
            message_instance = Pitt.objects.create(user=user, audio_content=up_file,
                                                   text_content=text_content)
            serializer = PublicationSerializer(data=message_instance.__dict__)

            if not serializer.is_valid():
                return Response({'error': serializer.errors})
            else:
                emails = []
                people_to_notify = user.get_followers()
                for subs in people_to_notify:
                    send_pitt_notification.delay(str(my_name), str(subs.username))
                # data = UserSerializer(people_to_notify, many=True)

                message_instance.save()
                return Response({'message': 'Your message was uploaded', "info": serializer.data}, status=200)
                # "people that will be notified": data.data}, status=200)


class DeleteaPitt(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):

        user = request.user
        id = request.data.get('id', None)
        if not id:
            return Response({'message': ' Blank line for pitts id is not allowed'}, status=400)

        try:
            pitt = Pitt.objects.get(id=id, user=user)
        except ObjectDoesNotExist:
            return Response({'error': 'Could not find this pitt in a database'}, status=400)
        data = pitt.__dict__
        serializer = PublicationSerializer(data=data)
        if serializer.is_valid():
            pitt.delete()
            return Response({'message': 'This pitt was deleted'}, status=200)
        else:
            return Response(serializer.errors)
