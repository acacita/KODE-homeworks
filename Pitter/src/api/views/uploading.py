from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from ..models.message_model import Message
from ..models.message_serializers import PublicationSerializer
from ..models.user_models import User
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist


class CreatePitt(APIView):
    # todo AUTHORIZE
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        up_file = request.data.get('file', None)
        file_type = str(up_file).split('.')[-1]
        if not up_file:
            return Response({"message": "the file is missing"}, status=400)

        elif file_type != 'flac':
            return Response({"message": "please send only flac files"}, status=406)

        try:
            username = request.data.get('username', None)
            userinstance = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist in a database'}, status=400)

        text_content = request.data.get('text_content', None)

        if up_file and file_type == 'flac':
            message_instance = Message.objects.create(user=userinstance, audio_content=up_file,
                                                      text_content=text_content)
            serializer = PublicationSerializer(data=message_instance.__dict__)

            if not serializer.is_valid():
                return Response({"error": serializer.errors})

            else:
                message_instance.save()
                return Response({"message": "Your message was uploaded", "info": serializer.data}, status=200)
