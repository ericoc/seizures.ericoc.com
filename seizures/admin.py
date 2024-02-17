from django.contrib import admin
from django.contrib.auth.admin import Group

from .models import Seizure


# Set header and title text for /admin/
admin.site.index_title = "Seizures"
admin.site.site_header = "seizures.ericoc.com"
admin.site.site_title = "Administration"

# Disable "groups" in /admin/
admin.site.unregister(Group)


@admin.register(Seizure)
class SeizureAdmin(admin.ModelAdmin):
    """Seizure administration."""
    can_delete = False
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
    show_facets = admin.ShowFacets.ALWAYS

    # No additions/modifications/deletions. Only view.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="SSID", ordering="ssid")
    def ssid_name(self, obj):
        return obj.ssid or None
