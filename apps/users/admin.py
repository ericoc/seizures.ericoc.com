from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AddUserForm, EditUserForm


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    """User administration."""
    add_form = AddUserForm
    form = EditUserForm
    model = get_user_model()
    fieldsets = (
        (None, {"fields": (model.USERNAME_FIELD, model.EMAIL_FIELD)}),
        ("Name", {"fields": ("first_name", "last_name")}),
        ("Created", {"fields": ("created_at",), "classes": ("collapse",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Groups", {"fields": ("groups",), "classes": ("collapse",)}),
        ("User Permissions", {
            "fields": ("user_permissions",), "classes": ("collapse",)
        })
    )
    date_hierarchy = "created_at"
    filter_horizontal = ()
    list_display = (
        model.USERNAME_FIELD, "first_name", "last_name",
        "is_active", "is_staff", "is_superuser"
    )
    list_display_links = (model.USERNAME_FIELD, "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = (
        model.USERNAME_FIELD, model.EMAIL_FIELD, "first_name", "last_name"
    )
    readonly_fields = ("created_at",)
