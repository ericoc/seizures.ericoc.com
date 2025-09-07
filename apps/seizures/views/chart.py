from .base import SeizuresBaseView


class SeizuresChartView(SeizuresBaseView):
    """Highcharts view."""
    days = 365
    template_name = "chart.html"

    # TODO: Update SeizuresChartView query to chart days with zero (0) seizures:
    # https://github.com/ericoc/seizures.ericoc.com/issues/3
