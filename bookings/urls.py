from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.booking_create, name="booking_create"),
    path("success/<int:pk>/", views.booking_success, name="booking_success"),
    path("availability/", views.availability, name="availability"),
    path("my/", views.my_bookings, name="my_bookings"),
    path("signup/", views.signup, name="signup"),
]
