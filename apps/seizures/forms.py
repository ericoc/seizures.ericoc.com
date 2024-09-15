from django.forms import Form, DateTimeField, TextInput
from django.utils.timezone import localtime


class SeizuresSearchDateForm(Form):
    """Seizure search date form."""
    _attrs = {"type": "datetime-local"}
    start = DateTimeField(label="", widget=TextInput(attrs=_attrs))
    end = DateTimeField(label="", widget=TextInput(attrs=_attrs))

    def get_initial_for_field(self, field, field_name):
        # Set date inputs "max" attribute to current time.
        field.widget.attrs["max"] = localtime().strftime("%Y-%m-%dT%H:%M")
        return super().get_initial_for_field(field, field_name)
