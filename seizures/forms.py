from django import forms
from django.utils import timezone


class SeizureSearchDateForm(forms.Form):
    """
    Seizure search date form.
    """

    @staticmethod
    def get_max():
        """Format current time to fill in max value for datetime-local field."""
        return timezone.localtime().strftime("%Y-%m-%dT%H:%M:%S")

    search_date = forms.DateTimeField(
        help_text="",
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "datetime-local",
                "max": get_max(),
                "onchange": "chooseDate();"
            }
        )
    )
