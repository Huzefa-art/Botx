from pymongo import MongoClient
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
import ast

from dotenv import load_dotenv

load_dotenv()


def get_chat_history_mongo(user_id, profile_id):
    client = MongoClient(
    host=os.getenv('MONGO_HOST'),
    port=int(os.getenv('MONGO_PORT')),
    # username=os.getenv('MONGO_DB'),
    # password=os.getenv('MONGODB_PASSWORD'),
    authSource='admin'
    )

    db = client[os.getenv('MONGO_DB')]
    collection = db['chat_history']
    print("collection", collection)
    query = {'user_id_id': user_id, "profile_id_id":profile_id}
    print("query", query)
    documents = collection.find(query)
    print("document", documents)

    if documents:
        all_chats = []

        for document in documents:
            chat_str = document.get('chat', '[]') 
            chat_list = ast.literal_eval(chat_str)
            all_chats.extend(chat_list)

        # Now `all_chats` contains a list of all chat messages across all documents
        # print("my chat",all_chats)
        # print("my chat history", chat_history)
        return all_chats
        # return documents.get('chat', [])
    else:
        return []        
    
def update_chat_history_redis(redis_chat, profile_id, mongo_chat):

    profile_id_str = str(profile_id)
    if profile_id_str in redis_chat:
        for i in mongo_chat:
            redis_chat[profile_id_str].append(i)
    else:
        redis_chat[profile_id_str] = mongo_chat
    
    return redis_chat


class LoadChat(APIView):

    def get(self, request, profile_id):
        # profile_id = request.data.get("profile_id")
        if not request.user.is_authenticated:
            return Response({"error": "You're not logged in!"})
        else:
            user_id = request.user.id

            if 'chat_history' not in request.session:
                
                redis_chat =request.session['chat_history'] = {}
            else:
                redis_chat = request.session['chat_history']
                print("my redis_chat2", redis_chat)
            profile_id_str = str(profile_id)

            if profile_id_str in redis_chat:
                print("my session",request.session.get('chat_history'))

                return Response({'chat_history': redis_chat[profile_id_str]})
            else:
                # try:
                mongo_chat = get_chat_history_mongo(user_id,profile_id)
                update_chat_history_redis(redis_chat, profile_id, mongo_chat)
                # chat_history = ast.literal_eval(redis_chat[profile_id_str])
                print("my session",request.session.get('chat_history'))
                return Response({'chat_history': redis_chat[profile_id_str]}) 
            # except:
            #     return Response({'error':"profile id does not exist"})
        




