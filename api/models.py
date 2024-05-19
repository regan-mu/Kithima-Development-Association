from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

user_roles = {
    "Chairperson": "Chairperson",
    "Secretary": "Secretary",
    "Treasurer": "Treasurer",
    "Patron": "Patron"
}


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(choices=user_roles, max_length=100)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"


class Event(models.Model):
    """Contribution Events"""
    title = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    public_id = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        secret = secrets.token_hex(9)
        self.public_id = secret
        super().save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Member(models.Model):
    """
        Group members
    """
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    member_number = models.IntegerField(null=False, blank=False, unique=True)
    mobile_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["member_number"]

    def __str__(self):
        return f"{self.first_name} {self.mobile_number} {self.member_number}"


class Contribution(models.Model):
    """
        Member Contributions
    """
    event = models.ForeignKey(Event, related_name="contributions", on_delete=models.DO_NOTHING)
    member = models.ForeignKey(Member, related_name="contributions", on_delete=models.DO_NOTHING)
    amount = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name}: {self.member.member_number}"



