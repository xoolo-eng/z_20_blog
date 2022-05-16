from django.urls import path
from user.views import log_in, log_out, SignInView
from django.shortcuts import redirect
from django.urls import reverse

urlpatterns = [
    path("login/", log_in, name="login_page"),
    path("signin/", SignInView.as_view(), name="signin_page"),
    path("logout/", log_out, name="logout_page"),
    path("", lambda request: redirect(reverse("login_page"))),
]
