from .base import SeizuresBaseView


class SeizuresChartView(SeizuresBaseView):
    """Highcharts view."""
    days = 365
    template_name = "chart.html"
