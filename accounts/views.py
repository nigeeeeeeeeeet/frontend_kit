from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm


def _safe_next_url(request):
    """Повертає безпечний ?next=, або None."""
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def signup(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація пройшла успішно. Ласкаво просимо!")
            return redirect(_safe_next_url(request) or settings.LOGIN_REDIRECT_URL)
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_safe_next_url(request) or settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm(request)

    return render(
        request,
        "accounts/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Ви вийшли з акаунта.")
    return redirect(settings.LOGOUT_REDIRECT_URL)
