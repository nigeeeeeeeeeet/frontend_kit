from datetime import date

from django import forms

from rooms.models import Room

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["guest_name", "email", "room", "start_date", "end_date"]
        labels = {
            "guest_name": "Ваше ім'я",
            "email": "Електронна пошта",
            "room": "Кімната / місце",
            "start_date": "Дата початку",
            "end_date": "Дата завершення",
        }
        widgets = {
            "guest_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Іван Петренко"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "name@example.com"}
            ),
            "room": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room"].queryset = Room.objects.filter(
            is_active=True
        ).select_related("room_type")
        self.fields["room"].empty_label = "Оберіть кімнату"
        today = date.today().isoformat()
        self.fields["start_date"].widget.attrs["min"] = today
        self.fields["end_date"].widget.attrs["min"] = today

    def clean_start_date(self):
        start = self.cleaned_data["start_date"]
        if start < date.today():
            raise forms.ValidationError("Дата початку не може бути в минулому.")
        return start
