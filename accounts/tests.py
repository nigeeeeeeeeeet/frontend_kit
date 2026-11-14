from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def test_custom_user_model_is_used(self):
        self.assertEqual(User._meta.label, "accounts.User")

    def test_signup_creates_user_and_logs_in(self):
        resp = self.client.post(
            reverse("signup"),
            {
                "username": "ivan",
                "email": "ivan@example.com",
                "first_name": "Іван",
                "last_name": "Петренко",
                "phone": "+380501234567",
                "password1": "Str0ng-pass-123",
                "password2": "Str0ng-pass-123",
            },
        )
        self.assertRedirects(resp, reverse("room_list"))
        self.assertTrue(User.objects.filter(username="ivan").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user("a", "dup@example.com", "Str0ng-pass-123")
        resp = self.client.post(
            reverse("signup"),
            {
                "username": "b",
                "email": "dup@example.com",
                "password1": "Str0ng-pass-123",
                "password2": "Str0ng-pass-123",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_login_and_logout(self):
        User.objects.create_user("olga", "olga@example.com", "Str0ng-pass-123")
        resp = self.client.post(
            reverse("login"), {"username": "olga", "password": "Str0ng-pass-123"}
        )
        self.assertRedirects(resp, reverse("room_list"))
        self.client.post(reverse("logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_wrong_password(self):
        User.objects.create_user("olga", "olga@example.com", "Str0ng-pass-123")
        resp = self.client.post(
            reverse("login"), {"username": "olga", "password": "wrong"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class LoginRequiredTests(TestCase):
    def test_protected_views_redirect_anonymous(self):
        for name in ("my_bookings", "booking_create"):
            url = reverse(name)
            resp = self.client.get(url)
            self.assertRedirects(
                resp, f"{reverse('login')}?next={url}", msg_prefix=name
            )

    def test_login_redirects_back_to_next(self):
        User.objects.create_user("olga", "olga@example.com", "Str0ng-pass-123")
        url = reverse("my_bookings")
        resp = self.client.post(
            reverse("login"),
            {"username": "olga", "password": "Str0ng-pass-123", "next": url},
        )
        self.assertRedirects(resp, url)

    def test_open_redirect_is_blocked(self):
        User.objects.create_user("olga", "olga@example.com", "Str0ng-pass-123")
        resp = self.client.post(
            reverse("login"),
            {
                "username": "olga",
                "password": "Str0ng-pass-123",
                "next": "https://evil.example.com/",
            },
        )
        self.assertRedirects(resp, reverse("room_list"))
