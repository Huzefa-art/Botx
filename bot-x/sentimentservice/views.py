from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentAnalysisSerializer
from sentimentservice.utils import perform_emotion_analysis_on_frame

class SentimentAnalysisView(APIView):
    def post(self, request, format=None):
        serializer = SentimentAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data.get('image')

            if image:

                frame, sentiment, emotion = perform_emotion_analysis_on_frame(image)
                if frame is None:
                    return Response({'error': 'No faces detected in the image.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'sentiment': sentiment, 'emotion': emotion}, status=status.HTTP_200_OK)

            return Response({'error': 'No valid input provided.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

