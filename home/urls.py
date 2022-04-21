from django.urls import path
from home.views import home_view, about_view
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home/", home_view, name="home_page"),
    path("about/", about_view, name="about_page"),
    path("", lambda request: redirect(reverse("home_page"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
