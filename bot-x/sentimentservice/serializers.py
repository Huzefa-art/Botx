from rest_framework import serializers

class SentimentAnalysisSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
