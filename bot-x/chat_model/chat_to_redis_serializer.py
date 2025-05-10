from rest_framework import serializers
from accounts.models.profile_models import Profile

class ChatToRedisSerializer(serializers.Serializer):
    profile_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    message = serializers.CharField(max_length=50)
    
