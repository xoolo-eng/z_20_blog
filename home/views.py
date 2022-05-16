from django.shortcuts import render
from home.forms import FeedBackForm
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


def home_view(request):
    return render(request, "home.html", {})


def about_view(request):
    return render(request, "about.html", {})


def contacts_view(request):
    form = FeedBackForm()
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Ваш прошлый запрос еще не обработан")
                messages.add_message(request, messages.ERROR, "Попробуйте позже")
            return redirect(reverse("contacts_page"))
    context = {
        "feedback_form": form,
        "address": "3 East Ridgewood Avenue Los Angeles, CA 90022",
        "phones": ["+213 908 92034", "+415 123 89245"],
        "emails": ["support@mobster.com", "support@macodeid.com"]
    }
    return render(request, "contacts.html", context)
