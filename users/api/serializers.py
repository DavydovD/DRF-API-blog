from rest_framework import serializers
from django.contrib.auth.models import User
from blog.settings import EMAIL_HUNTER_KEY
from pyhunter import PyHunter


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'email': {'required': True},
                        'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, email):
        if not email.strip():
            raise serializers.ValidationError('must not be empty')
        hunter = PyHunter(EMAIL_HUNTER_KEY)
        email_varifier = hunter.email_verifier(email)
        if email_varifier['gibberish']:
            raise serializers.ValidationError("Email is gibberish")
        return email


