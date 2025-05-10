from chat_model.serializer import chat_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SessionExpire(APIView):
    def post(self ,request):

        chat_history = request.session.get('chat_history', [])
        session_id =request.session.session_key        
        print("my session key",session_id)
        user_id = request.data.get("user_id")
        # profile_id = request.data.get("profile_id")
        data = {
            "user_id": user_id,
            # "profile_id":profile_id,
            "session_id": session_id,  
            "chat": str(chat_history),

        }
        serializer = chat_serializer(data=data)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

            # serializer.save() 
            # return Response(serializer.data, status=status.HTTP_201_CREATED) 
            
