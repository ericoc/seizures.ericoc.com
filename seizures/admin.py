from django.contrib import admin
from django.contrib.auth.admin import Group

from seizures.models import Seizure


# Set header and title text for /admin/
admin.site.index_title = "Seizures"
admin.site.site_header = "seizures.ericoc.com"
admin.site.site_title = "Administration"

# Disable "groups" in /admin/
admin.site.unregister(Group)


@admin.register(Seizure)
class SeizureAdmin(admin.ModelAdmin):
    """Seizure administration."""
    date_hierarchy = "timestamp"
    fieldsets = (
        (
            None, {
                "fields": (
                    "timestamp", "device_name"
                )
            }
        ),
        (
            "Device", {
                "fields": (
                    "device_type", "battery", "brightness", "ssid", "volume"
                ),
                "classes": (
                    "wide",
                )
            }
        ),
        (
            "Location", {
                "fields": (
                    "address", "altitude", "latitude", "longitude"
                ),
                "classes": (
                    "wide",
                )
            }
        )
    )
    list_display = ("timestamp", "address", "device_type", "ssid_name")
    list_filter = ("device_name", "device_type", "ssid")
    readonly_fields = (
        "timestamp", "device_name", "device_type",
        "ssid", "ssid_name", "volume", "address", "altitude",
        "battery", "brightness", "latitude", "longitude"
    )
    search_fields = ("device_name", "device_type", "address", "ssid")

    # No additions/modifications/deletions. Only view.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    @admin.display(description="SSID", ordering="ssid")
    def ssid_name(self, obj):
        return obj.ssid or None
