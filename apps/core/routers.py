class SeizureRouter:
    """Database router routes seizures reads and writes to SQLite."""

    def db_for_read(self, model, **hints):
        if model._meta.required_db_vendor:
            if model._meta.required_db_vendor == "sqlite":
                return model._meta.app_label
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.required_db_vendor:
            if model._meta.required_db_vendor == "sqlite":
                return model._meta.app_label
        return "default"
