from django.contrib import admin

from .models import Room, RoomType


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "room_type", "capacity", "price", "is_active")
    list_filter = ("room_type", "is_active")
    search_fields = ("name", "description", "features")
    list_editable = ("price", "is_active")
