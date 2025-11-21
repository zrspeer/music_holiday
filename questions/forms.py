from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    def __init__(self, data=None, question=None, instance=None):
        super().__init__(data=data, instance=instance)

        label = ""
        required = True

        if question is not None:
            label = question.prompt
            required = question.required

        initial = None
        if instance is not None:
            initial = instance.value_text

        if question is not None and question.input_type == "radio":
            choices = []

            for choice in question.get_choices_list():
                choices.append((choice, choice))

            self.fields["value_text"] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=label,
                required=required,
                initial=initial,
            )

        else:
            field = self.fields["value_text"]
            field.label = label
            field.required = required
            field.widget = forms.Textarea(attrs={"cols": 80})

    class Meta:
        model = Answer
        fields = ["value_text"]


class PasscodeForm(forms.Form):
    code = forms.CharField(
        label="Access code", widget=forms.PasswordInput(attrs={"autocomplete": "off"})
    )
