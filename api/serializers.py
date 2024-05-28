from rest_framework import serializers
from .models import Member, Event, Contribution, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["username", "role", "password"]
        model = User
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        username = validated_data.pop("username", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password.strip())
        instance.username = username.lower().strip()
        instance.save()
        return instance


class ContributionSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['event'] = instance.event.title
        representation['member'] = f"{instance.member.first_name} {instance.member.last_name}"
        return representation

    class Meta:
        model = Contribution
        fields = ["id", "event", "member", "amount", "created_at"]


class MemberSerializer(serializers.ModelSerializer):
    contributions = ContributionSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ["id", "first_name", "last_name", "member_number", "mobile_number", "join_date", "contributions"]


class EventSerializer(serializers.ModelSerializer):
    contributions = ContributionSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "created_at", "public_id", "contributions"]


