from django.contrib import admin

from seizures.models import Seizure


# Set header and title text for /admin/
admin.site.site_header = "seizures.ericoc.com"
admin.site.site_title = "Administration"
admin.site.index_title = "Seizures"


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
                )
            }
        )
    )
    list_display = ("timestamp", "device_type", "address")
    list_filter = ("device_name", "device_type", "ssid")
    readonly_fields = (
        "timestamp", "device_name", "device_type", "battery", "brightness",
        "ssid", "volume", "address", "altitude", "latitude", "longitude"
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


