import calendar
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from rooms.models import Room, RoomType

from .emails import send_booking_email
from .forms import BookingForm
from .models import Booking


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            send_booking_email(booking)
            request.session["last_booking"] = booking.pk
            messages.success(
                request,
                "Бронювання створено! Лист із підтвердженням надіслано на вашу пошту.",
            )
            return redirect("booking_success", pk=booking.pk)
    else:
        initial = {}
        room_id = request.GET.get("room", "")
        if room_id.isdigit():
            initial["room"] = int(room_id)
        if request.user.is_authenticated:
            initial["guest_name"] = (
                request.user.get_full_name() or request.user.username
            )
            initial["email"] = request.user.email
        form = BookingForm(initial=initial)

    return render(request, "bookings/booking_form.html", {"form": form})


def booking_success(request, pk):
    booking = get_object_or_404(Booking.objects.select_related("room"), pk=pk)
    is_owner = request.user.is_authenticated and booking.user_id == request.user.id
    if request.session.get("last_booking") != booking.pk and not is_owner:
        return redirect("room_list")
    return render(request, "bookings/booking_success.html", {"booking": booking})


def availability(request):
    today = date.today()
    try:
        year, month = (int(x) for x in request.GET.get("month", "").split("-"))
        first = date(year, month, 1)
    except ValueError:
        first = today.replace(day=1)

    days_in_month = calendar.monthrange(first.year, first.month)[1]
    last = first.replace(day=days_in_month)
    days = [first.replace(day=d) for d in range(1, days_in_month + 1)]

    rooms = Room.objects.filter(is_active=True).select_related("room_type")
    selected_type = request.GET.get("type", "")
    if selected_type.isdigit():
        rooms = rooms.filter(room_type_id=int(selected_type))
    rooms = list(rooms)

    bookings = Booking.objects.filter(
        room__in=rooms, start_date__lte=last, end_date__gte=first
    ).exclude(status=Booking.Status.CANCELLED)

    busy = {}
    for b in bookings:
        start = max(b.start_date, first)
        end = min(b.end_date, last)
        for day in range(start.day, end.day + 1):
            busy.setdefault(b.room_id, set()).add(day)

    header = [{"n": d.day, "weekend": d.weekday() >= 5} for d in days]
    rows = [
        {
            "room": room,
            "cells": [
                {
                    "date": d,
                    "busy": d.day in busy.get(room.id, set()),
                    "weekend": d.weekday() >= 5,
                }
                for d in days
            ],
        }
        for room in rooms
    ]

    return render(
        request,
        "bookings/availability.html",
        {
            "first": first,
            "prev_month": (first - timedelta(days=1)).replace(day=1),
            "next_month": last + timedelta(days=1),
            "header": header,
            "rows": rows,
            "room_types": RoomType.objects.all(),
            "selected_type": selected_type,
        },
    )


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        "room", "room__room_type"
    )
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація пройшла успішно. Ласкаво просимо!")
            return redirect("room_list")
    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"
    return render(request, "registration/signup.html", {"form": form})
