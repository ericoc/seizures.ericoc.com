from django.conf import settings
from django.contrib.admin import site
from django.contrib.auth.admin import Group


# Set header and title text for /admin/
site.index_title = site.site_header = settings.WEBSITE_TITLE
site.site_title = "Administration"

# Disable "groups" in /admin/
site.unregister(Group)
