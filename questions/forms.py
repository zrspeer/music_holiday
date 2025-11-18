from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["value_text"]
        labels = {"value_text": ""}
        widgets = {"value_text": forms.Textarea(attrs={"cols": 80})}


class PasscodeForm(forms.Form):
    code = forms.CharField(
        label="Access code", widget=forms.PasswordInput(attrs={"autocomplete": "off"})
    )
