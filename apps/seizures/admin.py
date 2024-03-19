from django.contrib.admin import register, ModelAdmin, ShowFacets

from .models import Seizure


@register(Seizure)
class SeizureAdmin(ModelAdmin):
    """Seizure administration."""
    date_hierarchy = "timestamp"
    fieldsets = (
        (None, {"fields": ("timestamp", "device_name")}),
        ("Device", {
            "fields": (
                "device_type", "battery", "brightness", "ssid", "volume"
            ),
        }),
        ("Location", {
            "fields": ("address", "altitude", "latitude", "longitude"),
        })
    )
    list_per_page = 10
    list_display = ("timestamp", "device_type", "address", "ssid")
    list_filter = ("timestamp", "device_type", "ssid")
    search_fields = ("address", "device_name", "ssid")
    show_facets = ShowFacets.ALWAYS

    # No additions/modifications/deletions. Only view.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
