from django.urls import path
from chat_audio.views import AudioUploadView

urlpatterns = [
    path('upload/', AudioUploadView.as_view(), name='audio-upload'),
]
