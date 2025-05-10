from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.serializers import UploadProfileSerializer
from ..models import Profile

class UploadProfileView(APIView):

    def post(self, request):

        serializer = UploadProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def get(self, request, bot_id, format=None): 
    
        try:
            profile = Profile.objects.get(id=bot_id)
            
            # still need to fix the audio
            print(profile.audiofilename)
            profile_data = {
                "name": profile.name,
                "role": profile.role,
                "conversation" : profile.conversation,
            }
            return Response(profile_data)
        
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

