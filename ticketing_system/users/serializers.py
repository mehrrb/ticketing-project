from rest_framework import serializers
from .models import Users



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','password', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    
        
    # def create(self, validated_data):
    #     user = Users(
    #         email=validated_data['email'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()