from rest_framework import serializers
from chat_model.models import chat_model


class chat_serializer(serializers.ModelSerializer):
    class Meta:
        model = chat_model
        fields = ["profile_id","session_id", "chat","created_at", "user_id"]
        read_only_fields=["created_at"]


    
