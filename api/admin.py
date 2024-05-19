from django.contrib import admin
from .models import Event, Member, Contribution


# Register your models here.
class EventAdminModel(admin.ModelAdmin):
    list_display = ["title", "created_at", "public_id"]
    search_fields = ["title", "public_id"]
    list_per_page = 10


class MemberAdminModel(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "member_number", "mobile_number"]
    search_fields = ["first_name", "last_name", "member_number"]
    list_per_page = 10


class ContributionAdminModel(admin.ModelAdmin):
    list_display = ["member", "amount", "event", "created_at"]
    list_per_page = 10


admin.site.register(Event, EventAdminModel)
admin.site.register(Member, MemberAdminModel)
admin.site.register(Contribution, ContributionAdminModel)
