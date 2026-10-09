import django.apps


class AppConfig(django.apps.AppConfig):
    name = "combo_plugin_imio_iacitizen"
    verbose_name = "iA.Citizen"

    def get_before_urls(self):
        from . import urls

        return urls.urlpatterns
