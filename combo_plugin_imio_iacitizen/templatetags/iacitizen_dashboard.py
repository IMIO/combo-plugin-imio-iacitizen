from django import template
from django.utils.text import slugify

from ..dashboard import get_user_tiles, remove_tile_url

register = template.Library()


@register.simple_tag(takes_context=True)
def dashboard_tiles_by_query(context, key, connector):
    """Requêtes déjà présentes dans le tableau de bord de l'utilisateur -> URL de suppression."""
    user = getattr(context.get("request"), "user", None)
    if not user or not user.is_authenticated:
        return {}
    return {query: remove_tile_url(cell) for query, (tile, cell) in get_user_tiles(user, key, connector).items()}


@register.filter
def category_query(item, local_data):
    """Slug de la requête passerelle d'un terme du vocabulaire catégories + thématiques."""
    local_titles = {local["title"] for local in (local_data or {}).get("data") or []}
    if item.get("title") in local_titles:
        return "local-%s" % slugify(item["title"])[:120]
    return item.get("token")


@register.filter
def get_item(mapping, key):
    return (mapping or {}).get(key)
