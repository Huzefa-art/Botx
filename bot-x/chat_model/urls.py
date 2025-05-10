from django.urls import path
from chat_model.views.chat_view import ChatMessageView
from chat_model.views.sessionexpire_view import SessionExpire
from chat_model.views.chat_history_view import LoadChat

urlpatterns = [
    path('chat/', ChatMessageView.as_view(), name='chat_message_api'),
    path('chat_history/<int:profile_id>/', LoadChat.as_view(), name='chat_history'),
    path('session_expire/', SessionExpire.as_view(), name='session_expire')
]