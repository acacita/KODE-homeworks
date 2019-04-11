from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import FileSystemStorage
import os
from api.integration.speechrecognizing import  transcribe
from settings import MEDIA_ROOT


class UploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        up_file = request.data.get('file', None)
        file_type = str(up_file).split('.')[-1]

        if not up_file:
            return Response({"message": "the file is missing"}, status=400)

        elif file_type != 'flac':
            return Response({"message": "please send only flac files"}, status=406)

        if up_file and file_type == 'flac':
            fs = FileSystemStorage()
            filename = fs.save(up_file.name, up_file)
            filepath = os.path.join(MEDIA_ROOT, filename)
            print(filepath)
            file_url = fs.url(filename)
            try:
                f = transcribe(filepath)
                return Response({"message": f}, status=200)
            except Exception:
                return Response({'message': 'Could not recognize speech'})

