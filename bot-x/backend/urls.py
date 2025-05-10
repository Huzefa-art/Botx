from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat_model/', include('chat_model.urls')),
    path('sentiment/',include('sentimentservice.urls')),
    path('chat_audio/',include('chat_audio.urls'))
]
