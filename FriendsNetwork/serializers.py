from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']


class FriendRequestListSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'status', 'created_at']


class FriendshipSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']
