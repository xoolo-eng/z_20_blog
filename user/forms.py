from django import forms
from user.models import User
from django.contrib.auth import login, authenticate


class SignInForm(forms.ModelForm):
    password_repeat = forms.CharField(widget=forms.PasswordInput())
    _sys_users = ("admin", "administrator", "sys", "superuser")

    class Meta:
        model = User
        fields = ("username", "phone", "email", "password")
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        is_errors = False
        if self.cleaned_data.get("password") != self.cleaned_data.get("password_repeat"):
            is_errors = True
            self.add_error(
                "password", "Different values in fields 'password' and 'password_repeat'."
            )
        if self.cleaned_data.get("username") in self._sys_users:
            is_errors = True
            self.add_error("username", "Invalid username.")
        if is_errors:
            raise forms.ValidationError("Invalid form.")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(**dict(self.cleaned_data))
        if user is not None:
            self.user = user
            return self.cleaned_data
        self.add_error("username", "Invalid username")
        self.add_error("password", "Invalid password")
        raise forms.ValidationError("User not found")

    def auth(self, request):
        login(request, self.user)
