from django.shortcuts import render
from django.contrib.auth import authenticate, user_logged_in
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView, LoginView as KnoxLogoutAllView
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from .models import User
from .serializers import UserCreationSerializer, allUserProfileSerializer


# Create your views here.

class Knox(KnoxLoginView):

    def __init__(self, request, user, **kwargs):
        self.request = request
        self.request.user = user
        self.format_kwarg = self.get_format_suffix(**kwargs)

    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
            'email': request.user.email,
            'user': request.user.name,
            'message': "SUCCESS"
        }
        return data
    def authenticator(self):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            tokens = self.request.user.auth_token_set.filter(expiry__gt=now).order_by('created')
            token_cnt = tokens.count()
            if token_cnt >= token_limit_per_user:
                for cnt in range(token_cnt - token_limit_per_user + 1):
                    tokens[cnt].delete()
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(self.request.user, token_ttl)
        user_logged_in.send(sender=self.request.user.__class__,
                            request=self.request, user=self.request.user)
        return self.get_post_response_data(self.request, token, instance)


class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"msg": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        data = Knox(request, user, **kwargs).authenticator()
        return Response(data)


class LogoutView(KnoxLogoutView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({
            'message': "Successfully logged"
        }, status=HTTP_200_OK)


class LogoutAllView(KnoxLogoutAllView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({
            'message': "Successfully Logged Out"
        }, status=HTTP_200_OK)


class RegisterView(APIView):

    @staticmethod
    @csrf_exempt
    def post(request, **kwargs):
        serializer = UserCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            })
        user = serializer.save()
        data = Knox(request, user, **kwargs).authenticator()
        data.update({'msg': 'Registration Successful'})
        return Response(data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        return Response({
            'data': "Hello World"
        })
