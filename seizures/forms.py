from django import forms


class SeizuresSearchDateForm(forms.Form):
    """
    Seizure search date form.
    """

    search_start = forms.DateTimeField(
        help_text="", label="",
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )

    search_end = forms.DateTimeField(
        help_text="", label="",
        widget=forms.TextInput(attrs={"type": "datetime-local"})
    )

    def set_values(self, start, end, max_date):
        """Set initial search form values and maximum date values."""
        self.fields["search_start"].widget.attrs.update(
            {"value": start, "max": max_date}
        )
        self.fields["search_end"].widget.attrs.update(
            {"value": end, "max": max_date}
        )
