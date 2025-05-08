from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm


class AddUserForm(AdminUserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            model.USERNAME_FIELD, model.EMAIL_FIELD, "first_name", "last_name",
            "is_active", "is_staff", "is_superuser"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class EditUserForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            model.USERNAME_FIELD, model.EMAIL_FIELD, "first_name", "last_name",
            "is_active", "is_staff", "is_superuser"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
