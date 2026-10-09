if "combo_plugin_imio_iacitizen" not in INSTALLED_APPS:
    INSTALLED_APPS += ("combo_plugin_imio_iacitizen",)
    TENANT_APPS += ("combo_plugin_imio_iacitizen",)

_CONNECTOR_FIELD = {
    "label": "Identifiant du connecteur Plone REST API",
    "type": "string",
    "varname": "connector",
}
_FIELD_CHOICES_URL = "{{ passerelle_url }}plone-restapi/{{ connector }}/get_field_choices?id="

JSON_CELL_TYPES.update(
    {
        "evenements-categories": {
            "name": "Événements - choix des catégories",
            "cache_duration": 120,
            "force_async": False,
            "log_errors": False,
            "form": [_CONNECTOR_FIELD],
            "url": _FIELD_CHOICES_URL + "imio.events.vocabulary.EventsCategoriesAndTopicsVocabulary",
            "additional-data": [
                {"key": "local", "url": _FIELD_CHOICES_URL + "imio.events.vocabulary.EventsLocalCategories"},
            ],
        },
        "actualites-categories": {
            "name": "Actualités - choix des catégories",
            "cache_duration": 120,
            "force_async": False,
            "log_errors": False,
            "form": [_CONNECTOR_FIELD],
            "url": _FIELD_CHOICES_URL + "imio.news.vocabulary.NewsCategoriesAndTopicsVocabulary",
            "additional-data": [
                {"key": "local", "url": _FIELD_CHOICES_URL + "imio.news.vocabulary.NewsLocalCategories"},
            ],
        },
    }
)
