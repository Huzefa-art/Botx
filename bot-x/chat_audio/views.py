from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import default_storage
from django.conf import settings
from .models import AudioFile
from .serializers import AudioFileSerializer
from .transcriber import speech_to_text
from .voice_clone import VoiceCloner
import os
import requests
from rest_framework import status

class AudioUploadView(APIView):
    # parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = request.data['audio']
            path = default_storage.save(f'audio_files/{audio_file.name}', audio_file)
            # full_path = os.path.join(settings.MEDIA_ROOT, path)
            return Response(audio_file.name, status=status.HTTP_201_CREATED) 

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        print("my input audio path",path)
        transcript = speech_to_text(full_path)
        print(transcript)

        if transcript is None:
            return Response({"error": "Transcription failed"}, status=500)

        data = {
            'message': transcript,
            'profile_id': 1
        }
        response = requests.post(
            'http://127.0.0.1:8000/chat_model/chat/', 
            json=data
        )
        response_data = response.json()

        bot_reply = response_data.get('message')

        cloner = VoiceCloner()
        response_audio_path = cloner.clone_voice(
            bot_reply, 
            full_path, 
            f'output_{audio_file.name}'
        )

        return Response({
            'response_audio_url': default_storage.url(response_audio_path),
        })
