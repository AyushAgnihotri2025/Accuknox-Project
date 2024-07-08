from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.decorators import throttle_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from Accounts.models import User
from FriendsNetwork.models import FriendRequest, Friendship
from FriendsNetwork.serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer, \
    FriendRequestListSerializer


# Create your views here.

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        keyword = request.data.get('keyword', '')
        if '@' in keyword:
            users = User.objects.filter(email__iexact=keyword)
        else:
            users = User.objects.filter(Q(name__icontains=keyword))

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        try:
            receiver_id = request.data.get('receiver_id')
            if receiver_id is None:
                return Response({"error": "User Doesn't Exits"}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.pk == receiver_id:
                return Response({"error": "Sender and Receiver Can't Same"}, status=status.HTTP_400_BAD_REQUEST)

            receiver = User.objects.get(id=receiver_id)

            # Check friend request limit
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests = FriendRequest.objects.filter(sender=request.user, created_at__gte=one_minute_ago).count()
            if recent_requests >= 3:
                return Response({"error": "You can only send 3 friend requests per minute."},
                                status=status.HTTP_400_BAD_REQUEST)

            if FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
                return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

            if FriendRequest.objects.filter(receiver=request.user, sender=receiver).exists():
                return Response({"error": "User is already your Friend."}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            Response({"error": "User Doesn't Exits"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            friend_request_id = request.data.get('request_id')
            action = request.data.get('action')

            if friend_request_id is None:
                return Response({"error": "Friend Request Id Can't Be None"}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest.objects.get(id=friend_request_id)

            if action == 'accept':
                friend_request.accept()
            elif action == 'reject':
                friend_request.reject()
            else:
                return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            Response({"error": "Friend Request Id Doesn't Exits"}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(FriendshipSerializer(Friendship.objects.filter(user=self.request.user), many=True).data,
                        status=status.HTTP_200_OK)


class ListPendingFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(FriendRequestListSerializer(FriendRequest.objects.filter(receiver=self.request.user, status=1),
                                                    many=True).data,
                        status=status.HTTP_200_OK)


class ListSentPendingFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(FriendRequestListSerializer(FriendRequest.objects.filter(sender=self.request.user, status=1),
                                                    many=True).data,
                        status=status.HTTP_200_OK)


class ListRejectedFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(FriendRequestListSerializer(FriendRequest.objects.filter(receiver=self.request.user, status='3'),
                                                    many=True).data,
                        status=status.HTTP_200_OK)
