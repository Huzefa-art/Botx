import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.serializers import SignUpSerializer, LoginSerializer
from accounts.renderers import UserRenderer

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
import requests
from django.middleware.csrf import get_token
from chat_model.serializer import chat_serializer
# Create your views here.

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    # permission_classes = [AllowAny]
    def get(self, request):
        return Response({"details" : "CSRF Cookies Set"})


# @method_decorator(csrf_protect, name='dispatch')
class SignUpView(APIView):
    # permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # confirmation email
            """"code block"""

            return Response({"details": "Registration Successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    # permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            user = authenticate(email=email, password=password)
            print("my user",user.id)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    session = request.session
                    print("My session:",session)
                    print(request.session.session_key)
                    
                    return Response({"details": "Logged in Succesfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors": ['Email or Password is not valid']}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    
    def post(self, request):

        if not request.user.is_authenticated:
            return Response({"logout detail": "You're not logged in!"})
        else:
            user = request.user
            saved_chats = []
            session_data = request.session.get('chat_history', {})  # Retrieve all session data under 'chat_history'
            print("session data", session_data)
            if session_data:
                for profile_id, messages in session_data.items():
                    print("my session data",session_data)
                    print("my profile id",profile_id)
                    print("messages",messages)

                    document = {
                        'session_id' : request.session.session_key,
                        'user_id': user.id,
                        'profile_id': profile_id,
                        'chat': str(messages)
                    
                    }

                    serializer = chat_serializer(data=document)

                    if serializer.is_valid():
                        serializer.save() 
                        print("save to mongodb successfully")
                        saved_chats.append(serializer.data)
                    else:
                        return Response({"error": "Failed to save chat data", "details": serializer.errors},
                                        status=status.HTTP_400_BAD_REQUEST)

        logout(request)

        return Response({"Mongodb status": saved_chats, "logout detail": "Logged out Successfully!"}, status=status.HTTP_200_OK)
            
        # csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
        # if not csrf_token:
        #     return Response({"detail": "CSRF token missing"}, status=400)
        # print("my csrf token",csrf_token)

        # url = "http://127.0.0.1:8000/chat_model/session_expire/"

        # data = {
        #     "user_id": "1"
        # }

        # headers = {
        #     "X-CSRFToken": csrf_token,
        #     "Content-Type": "application/json"
        # }

        # response = requests.post(url, json=data, headers=headers)
        # # print("Status Code:", response.status_code)
        # # print("Response JSON:", response.json())
        # return Response({"Status Code:", response.content}, status=status.HTTP_200_OK)
        # return Response({"detail": "Logged out Successfully!"}, status=status.HTTP_200_OK)

# def save_to_mongo_db(request):
#     chat_history = request.session.get('chat_history', [])
#     session_id =request.session.session_key        
#     print("my session key",session_id)
#     user_id = request.data.get("user_id")
#     # profile_id = request.data.get("profile_id")
#     data = {
#         "user_id": user_id,
#         # "profile_id":profile_id,
#         "session_id": session_id,  
#         "chat": str(chat_history),

#     }
#     serializer = chat_serializer(data=data)
#     return serializer



# def get_chat_history(request, user_id, profile_id):
#     try:
#         chat_history = ChatModel.objects.using('chat_db').filter(user_id=user_id, profile_id=profile_id)
#         if chat_history.exists():
#             serializer = chat_serializer(chat_history, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"message": "No chat history found for the given user and profile IDs."}, status=404)
#     except ChatModel.DoesNotExist:
#         return Response({"message": "Chat history does not exist."}, status=404)
