from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.detail import DetailView
from user.forms import SignInForm, LoginForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from user.models import User


class UserView(ListView):
    model = User
    template_name = "users.html"
    paginate_by = 2


class UserDetailView(TemplateView):
    template_name = "user.html"


def log_in(request):
    if request.user.is_authenticated:
        return redirect("home_page")
    context = {"login_form": LoginForm()}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.auth(request)
            next_url = request.GET.get("next")
            if next_url is not None:
                return redirect(next_url)
            return redirect(reverse("home_page"))
        context.update(login_form=login_form)
    return render(request, "login.html", context)


class SignInView(FormView):
    template_name = "signin.html"
    form_class = SignInForm

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url is not None:
            return next_url
        return reverse("login_page")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("login_page"))
