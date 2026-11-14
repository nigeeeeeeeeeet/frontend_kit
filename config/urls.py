from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("bookings/", include("bookings.urls")),
    path("", include("rooms.urls")),
]
