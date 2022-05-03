from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class MovieSerializer(serializers.ModelSerializer):
    cast = serializers.SlugRelatedField(
        many=True, slug_field='firstname', read_only=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Movie
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'birthdate')

    email = serializers.EmailField(max_length=254, required=True)
    phone = serializers.CharField(max_length=25, allow_null=True,  required=False)
    birthdate = serializers.DateField(allow_null=True, required=False)

    def validate_password(self, password):
        if len(password) < 5:
            raise serializers.ValidationError(
                'password must consist at least 5 characters')
        return password

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'password')

    email = serializers.EmailField(max_length=254, required=True)