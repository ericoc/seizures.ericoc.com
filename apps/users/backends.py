from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserAuthBackend(ModelBackend):
    """User authentication backend."""
    create_unknown_user = False
    model = get_user_model()

    def get_user(self, id=None):
        # Get a user by ID.
        return self.model.objects.get(id=id)
