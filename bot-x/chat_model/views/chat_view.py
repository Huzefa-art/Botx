from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from chat_model.config import *
from chat_model.chatbot import chat_openai, chat_prompt_template
from chat_model.prompts import system_message
from typing import Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from chat_model.chat_to_redis_serializer import ChatToRedisSerializer


from dotenv import load_dotenv

load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)



def save_message_to_session(request, user_message, ai_response,profile_id):
    redis_chat = request.session.get('chat_history')
    print("my redis chat", redis_chat)
    if 'chat_history' not in request.session:
        print("my redis was empty?",type(request.session),request.session)
        request.session['chat_history'] = {}
    print("redis before adding current chat", request.session['chat_history'])
    if profile_id not in request.session['chat_history']:
        request.session['chat_history'][profile_id] = []

    request.session['chat_history'][profile_id].append({"user_message": user_message, "ai_response": ai_response})
    print("redis before after adding current chat", request.session['chat_history'])

    
    # mongo_db = [{'user_message': 'tell me about yourself and also tell me how is your father', 'ai_response': 'I can answer you that.'}]

    # update_chat_history(chat_history, 26, mongo_db)

    print("chat_history",request.session['chat_history'])

    # Save session to write changes to Redis
    request.session.modified = True

def get_chat_history_from_session(request):
    return request.session.get('chat_history', [])

class ChatMessageView(APIView):

    def post(self, request):

        # post_param = request.POST.get('param_name')             # For POST parameters
        # uploaded_file = request.FILES.get('file_name')          # For file uploads
        # cookie_value = request.COOKIES.get('cookie_name')       # For cookies
        # user_agent = request.META.get('HTTP_USER_AGENT')        # For request metadata (like headers)
        serializer = ChatToRedisSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            user_message = data.get('message')
            profile_id = data.get('profile_id')
            # return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not user_message:
            return Response({"error":"Missing message"}, status=status.HTTP_404_NOT_FOUND)
        
        
        config = {
            'name': 'saif', 
            'relation': 'friend',
            'converted_format': "hello: hi",
            'sentiment': 'sad',
            'emotion': 'sad',
            'system_message': system_message,
        }
        bot_reply,memory = reply(user_message, config)
    
        # if request.session.test_cookie_worked() == False:
        #     request.session.set_test_cookie()

        save_message_to_session(request,user_message,bot_reply,profile_id )

        print(get_chat_history_from_session(request))

        # session.set_expiry(0)
        # session.set_expiry(10)
        # session.clear_expired()

        # print("set test cookie:",session.test_cookie_worked())
        # print("my session",session.keys())
        # # print(request.session['my_chat'])
        session = request.session

        print("session expiry data:", session.get_expiry_date())
        print("session expiry age:", session.get_expiry_age())
        print("expiry set on browser close:",session.get_expire_at_browser_close())
        print(request.session.session_key)
        # print("this is my memory",memory)
        return Response({'message': bot_reply })



# -----------------------------------------------------------------------------

def reply(question, config):

    chain, memory = conversation_chain(config)
    try:
        output = chain.invoke(question)
    except:
        output = {"text":chain}
    
    return output['text'],memory


# Chain
def conversation_chain(config: Dict[str, Any]) -> LLMChain:
    """
    Creates a conversation chain.

    Args:
    config (Dict[str, Any]): 
    A dictionary containing configuration parameters 
    for the conversation chain, including user details.

    Returns:
    Returns an instance of LLMChain
    """
    try:
        conversation = LLMChain(
            llm=chat_openai('gpt-3.5-turbo'),
            prompt=chat_prompt_template(
                {'name': config.get('name', ''), 
                 'relation': config.get('relation', ''),
                 'chat': config.get('converted_format', ''),
                 'sentiment': config.get('sentiment', ''),
                 'emotion': config.get('emotion', ''),},
                system_message_template=config.get('system_message', '')
            ),
            verbose=False,
            memory=memory
        )
        print("conversation",conversation,memory)
        return conversation, memory

    except Exception as error:
        # conversation = "I can answer you that."
        # memory = config.get('system_message', '')
        print(f"Error creating conversation chain: {error}")
        # return conversation, memory 
  


