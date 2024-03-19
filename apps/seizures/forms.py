from django.forms import Form, DateTimeField, TextInput


class SeizuresSearchDateForm(Form):
    """Seizure search date form."""
    _attrs = {"type": "datetime-local"}
    start = DateTimeField(label="", widget=TextInput(attrs=_attrs))
    end = DateTimeField(label="", widget=TextInput(attrs=_attrs))
