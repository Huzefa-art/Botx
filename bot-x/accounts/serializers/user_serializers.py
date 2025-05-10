from rest_framework import serializers
from accounts.models import User



class SignUpSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)    
    class Meta:

        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            "password": {'write_only': True}
        }

    # check password validation
    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        return data

    def create(self, validated_data):
        return User.object.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=50)
    class Meta:

        model = User
        fields = ["email", "password"]


