from django import forms
from home.models import FeedBack


class FeedBackForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "full_name"},
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "email"},
        )
    )
    phone = forms.CharField(
        label="Phone optional :)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "phone"},
        )
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "id": "message", "rows": "6"}
    ))

    def clean(self):
        if self.cleaned_data.get('full_name') == "Bacya Pupkin":
            self.add_error("full_name", "Хватит нам писать")
            self.add_error("full_name", "WTF?")
            raise forms.ValidationError("Что то тут не так")
        return self.cleaned_data

    def save(self):
        feedback = FeedBack(**self.cleaned_data)
        feedback.save()


