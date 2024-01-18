from . import SeizuresBaseView


class SeizuresSSIDView(SeizuresBaseView):
    """Search for seizures from a specific SSID network name."""

    def get_queryset(self):
        """Filter seizures from the requested SSID."""
        self.extra_context = {"search_ssid": self.kwargs["search_ssid"]}
        return super().get_queryset().filter(
            ssid__exact=self.kwargs["search_ssid"]
        )
