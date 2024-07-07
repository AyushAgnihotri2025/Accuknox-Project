"""
URL configuration for AccuKnox Project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from FriendsNetwork.views import SearchView, ListFriendsView, ListPendingFriendRequestView, FriendRequestView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search_users'),
    path('friend-request/', FriendRequestView.as_view(), name='accept_friend_request'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
    path('list_pending_friend_requests/', ListPendingFriendRequestView.as_view(), name='list_pending_friend_requests'),
]