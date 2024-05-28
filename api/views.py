import datetime
import jwt
import os

import permission as permission
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, Member, User, Contribution
from .serializers import MemberSerializer, EventSerializer, UserSerializer, ContributionSerializer


class CreateUsersAPIView(APIView):
    """List and create members"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    """Login the user"""

    def post(self, request):
        username = request.data["username"].lower().strip()
        password = request.data["password"].strip()

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User Not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, os.getenv("DJANGO_SECRET"), algorithm="HS256")

        response = Response()
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600,
        )

        response.data = {"token": token}
        return response


class RetrieveUserAPIView(APIView):
    """"Retrieve single user"""

    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("User not Authenticated")
        try:
            payload = jwt.decode(token, os.getenv("DJANGO_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed("User not Authenticated")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    """Logout User"""

    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "Logged Out"}
        return response


class CreateListMembersAPIView(generics.ListCreateAPIView):
    """List and create members"""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class RetrieveMemberAPIView(APIView):
    """Retrieve Member"""

    def get_object(self, member_number):
        member = Member.objects.filter(member_number=member_number).first()
        return member

    def get(self, request, member_number):
        member = self.get_object(member_number)
        if member is None:
            return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member)
        return Response(serializer.data)


class ListCreateEvent(generics.ListCreateAPIView):
    """List Create Event"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RetrieveEventAPIView(generics.RetrieveAPIView):
    """Retrieve single Event"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ListCreateContributionAPIView(generics.ListCreateAPIView):
    """List and Add Contribution"""

    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer

    def post(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        if not token:
            raise AuthenticationFailed("User not Authenticated")
        try:
            payload = jwt.decode(token, os.getenv("DJANGO_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed("User not Authenticated")

        data = request.data
        member = Member.objects.filter(id=data["member_id"]).first()
        event = Event.objects.filter(id=data["event_id"]).first()

        if member is None:
            raise NotFound("Member Not found")

        if event is None:
            raise NotFound("Event not found")

        contribution = Contribution.objects.filter(event=data["event_id"], member=data["member_id"]).first()
        if contribution is not None:
            return Response("Member has already contributed for this event", status=status.HTTP_400_BAD_REQUEST)

        contribution_data = {
            "event": event.id,
            "member": member.id,
            "amount": data.get("amount")
        }

        serializer = ContributionSerializer(data=contribution_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
