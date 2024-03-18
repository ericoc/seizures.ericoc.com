from .base import SeizuresBaseView


class SeizuresSSIDView(SeizuresBaseView):
    """Search for seizures from a specific SSID network name."""
    search_ssid = None

    def dispatch(self, request, *args, **kwargs):
        """Find SSID that is being searched for."""
        self.search_ssid = kwargs.get("search_ssid", None)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Include searched SSID in context."""
        context = super().get_context_data(*args, **kwargs)
        context["search_ssid"] = self.search_ssid
        return context

    def get_queryset(self):
        """Filter seizures from the requested SSID."""
        qs = super().get_queryset()
        if self.search_ssid:
            return qs.filter(ssid__iexact=self.search_ssid)
        return qs
