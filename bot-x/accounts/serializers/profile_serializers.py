from rest_framework import serializers
from accounts.models import Profile
from ..utility_functions import remove_date_and_time, convert_into_list_of_dictionary



class UploadProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    filename = serializers.FileField(write_only=True)
    class Meta:

        model = Profile
        fields = ["name", "role", "filename", "audiofilename", "created_at", "user"]
        read_only_fields=["conversation","created_at"]

    def create(self, validated_data):
        filename = validated_data.pop('filename', None)
        profile = super().create(validated_data)

        if filename:
            file_content = filename.read().decode('utf-8')

            # Data Formatting
            remove_date_time = remove_date_and_time(file_content)
            conversation = convert_into_list_of_dictionary(remove_date_time)

            profile.conversation = conversation
            profile.save()

        return profile

