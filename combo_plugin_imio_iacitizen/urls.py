from django.urls import re_path

from .views import dashboard_tiles

urlpatterns = [
    re_path(
        r"^api/iacitizen/dashboard-tiles/(?P<key>[\w_-]+)/$",
        dashboard_tiles,
        name="iacitizen-dashboard-tiles",
    ),
]
