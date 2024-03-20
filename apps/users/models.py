from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import (
    MinLengthValidator, MaxLengthValidator, EmailValidator
)
from django.db import models
from django.utils.html import format_html
from libgravatar import Gravatar, sanitize_email


class UserManager(BaseUserManager):
    """User database query manager."""

    def create_user(
        self, username=None, email=None, password=None,
        is_staff=False, is_superuser=False
    ):
        """
        Create and save user with given username, e-mail address, and password.
        """
        if not username:
            raise ValueError("User name is required.")

        user = self.model(
            username=username, email=email, is_active=True,
            is_staff=is_staff, is_superuser=is_superuser
        )
        user.set_unusable_password()
        if password:
            user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None):
        """Create and save user as a superuser."""
        user = self.create_user(
            username=username, email=email, password=password,
            is_staff=True, is_superuser=True
        )
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """User account."""
    id = models.AutoField(
        db_column="id",
        primary_key=True,
        help_text="User identification number.",
        verbose_name="User ID"
    )
    username = models.SlugField(
        db_column="username",
        help_text="Username for the user account.",
        max_length=16,
        unique=True,
        validators=(
            MinLengthValidator(limit_value=3),
            MaxLengthValidator(limit_value=16)
        ),
        verbose_name="Username"
    )
    email = models.EmailField(
        db_column="email",
        default=None,
        max_length=64,
        null=True,
        help_text="E-mail address for the user account.",
        validators=(
            MinLengthValidator(limit_value=5),
            MaxLengthValidator(limit_value=64),
            EmailValidator()
        ),
        verbose_name="E-mail Address"
    )
    first_name = models.CharField(
        db_column="first_name",
        default=None,
        max_length=32,
        null=True,
        help_text="First name for the user account.",
        verbose_name="First Name"
    )
    last_name = models.CharField(
        db_column="last_name",
        default=None,
        max_length=32,
        null=True,
        help_text="Last name for the user account.",
        verbose_name="Last Name"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at",
        help_text="Date and time when the user account was created.",
        verbose_name="Created At"
    )
    is_active = models.BooleanField(
        db_column="is_active",
        default=True,
        help_text="Is the user active?",
        verbose_name="Active?"
    )
    is_staff = models.BooleanField(
        db_column="is_staff",
        default=False,
        help_text="Is the user staff?",
        verbose_name="Staff?"
    )
    is_superuser = models.BooleanField(
        db_column="is_superuser",
        default=False,
        help_text="Is the user a superuser?",
        verbose_name="Superuser?"
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    objects = UserManager()
    last_login = None
    REQUIRED_FIELDS = (EMAIL_FIELD,)

    def get_email_link(self) -> str:
        email = getattr(self, self.get_email_field_name())
        return format_html(
            '<a href="mailto:%s" target="_blank" title="E-mail %s">%s</a>' % (
                email, email, email
            )
        )

    def get_full_name(self) -> str:
        return "%s %s".strip() % (self.first_name, self.last_name)

    def get_gravatar(self) -> str:
        return Gravatar(email=sanitize_email(email=self.email)).get_image()

    def get_short_name(self) -> str:
        if self.first_name:
            return self.first_name
        return self.get_username()

    class Meta:
        db_table = "users"
        db_table_comment = "Users."
        default_related_name = "user"
        managed = True
        ordering = ("id",)
        verbose_name = "User"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.get_username()
