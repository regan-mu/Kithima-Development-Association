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


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ["id", "first_name", "last_name", "member_number", "mobile_number", "join_date"]


class ContributionSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    # def create(self, validated_data):
    #     member_data = validated_data.pop("member", None)
    #     member_instance = None
    #     if member_data:
    #         member_instance, _ = Member.objects.get_or_create(**member_data)
    #
    #     contribution = Contribution.objects.create(member=member_instance, **validated_data)
    #
    #     return contribution

    class Meta:
        model = Contribution
        fields = ["id", "event", "member", "amount", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    contributions = ContributionSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "created_at", "public_id", "contributions"]


