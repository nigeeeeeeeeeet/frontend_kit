from django.shortcuts import render

from .models import Room, RoomType


def room_list(request):
    rooms = Room.objects.filter(is_active=True).select_related("room_type")
    selected_type = request.GET.get("type", "")
    if selected_type.isdigit():
        rooms = rooms.filter(room_type_id=int(selected_type))

    return render(
        request,
        "rooms/room_list.html",
        {
            "rooms": rooms,
            "room_types": RoomType.objects.all(),
            "selected_type": selected_type,
        },
    )
