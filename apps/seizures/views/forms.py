from django import forms


class SeizuresSearchDateForm(forms.Form):
    """Seizure search date form."""
    search_start = forms.DateTimeField(
        help_text="",
        label="",
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )
    search_end = forms.DateTimeField(
        help_text="",
        label="",
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )

    def set_values(self, start: str, end: str):
        """Set initial search form values and maximum date values."""
        self.fields["search_start"].initial = start
        self.fields["search_end"].initial = end