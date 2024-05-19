from rest_framework.urls import path
from .views import (
    CreateListMembersAPIView, RetrieveMemberAPIView,
    CreateUsersAPIView, UserLoginAPIView, RetrieveUserAPIView, LogoutAPIView,
    ListCreateEvent, RetrieveEventAPIView,
    ListCreateContributionAPIView
)

urlpatterns = [
    path("members", CreateListMembersAPIView.as_view()),
    path("member/<int:member_number>", RetrieveMemberAPIView.as_view()),
    path("users", CreateUsersAPIView.as_view()),
    path("user", RetrieveUserAPIView.as_view()),
    path("login", UserLoginAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
    path("events", ListCreateEvent.as_view()),
    path("event/<int:pk>", RetrieveEventAPIView.as_view()),
    path("contributions/", ListCreateContributionAPIView.as_view())
]
