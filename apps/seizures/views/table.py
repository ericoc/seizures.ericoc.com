from .base import SeizuresBaseView


class SeizuresTableView(SeizuresBaseView):
    """DataTables view."""
    days = 90
    template_name = "table.html"
