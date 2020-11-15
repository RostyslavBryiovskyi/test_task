from rest_framework import serializers
from .models import Order, Product, Profile
from django.contrib.auth.models import User
from test_task import settings
import datetime


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer
    """
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        """
        Get user first_name
        """
        return obj.user.first_name

    def get_last_name(self, obj):
        """
        Get user last_name
        """
        return obj.user.last_name

    def get_date_joined(self, obj):
        """
        Get user date_joined
        """
        return obj.user.date_joined.strftime("%d-%m-%Y")

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name',  'date_of_birth', 'date_joined', 'order']


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'password', 'password2', 'last_name', 'username']
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True}}

    def create(self, validated_data):
        """
        User creation if serializer is valid and user
        with the same username doesn`t exist
        """
        username = validated_data['username']
        firstname = validated_data['first_name']
        lastname = validated_data['last_name']
        password = validated_data['password']
        password2 = validated_data['password2']
        try:
            user = User.objects.get(username=username)
            raise serializers.ValidationError(
                {'username': 'User with this username already exist.'}
            )
        except Exception as e:
            if password != password2:
                raise serializers.ValidationError({'password': 'The two passwords differ.'})
            user = User(
                username=username,
                first_name=firstname,
                last_name=lastname,
            )
            user.set_password(password)
            user.save()
            return user
