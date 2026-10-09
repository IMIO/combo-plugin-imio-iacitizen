from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max, Min
from django.urls import reverse

from combo.apps.dashboard.models import DashboardCell, Tile
from combo.data.models import ConfigJsonCell


def get_user_tiles(user, key, connector):
    """Tuiles {key, connector} du tableau de bord de l'utilisateur, par requête."""
    cell_type = ContentType.objects.get_for_model(ConfigJsonCell)
    tiles = {
        tile.cell_pk: tile
        for tile in Tile.objects.filter(user=user, dashboard__isnull=False, cell_type=cell_type)
    }
    result = {}
    for cell in ConfigJsonCell.objects.filter(pk__in=list(tiles), key=key):
        if cell.parameters.get("connector") == connector:
            result[cell.parameters.get("query")] = (tiles[cell.pk], cell)
    return result


def remove_tile_url(cell):
    return reverse("combo-dashboard-remove-tile", kwargs={"cell_reference": cell.get_reference()})


def add_tiles(user, key, connector, queries):
    """Ajoute une tuile par requête absente ; renvoie {requête: URL de suppression}."""
    dashboard = DashboardCell.objects.filter(page__snapshot__isnull=True).first()
    if dashboard is None:
        return None
    existing = get_user_tiles(user, key, connector)
    user_tiles = Tile.objects.filter(dashboard=dashboard, user=user)
    first = settings.COMBO_DASHBOARD_NEW_TILE_POSITION == "first"
    if first:
        order = user_tiles.aggregate(Min("order"))["order__min"]
        order = order - 1 if order is not None else 0
    else:
        order = user_tiles.aggregate(Max("order"))["order__max"]
        order = order + 1 if order is not None else 0
    result = {}
    for query in queries:
        if query in existing:
            result[query] = remove_tile_url(existing[query][1])
            continue
        cell = ConfigJsonCell.objects.create(
            page=dashboard.page,
            placeholder="_dashboard",
            order=1,
            key=key,
            parameters={"connector": connector, "query": query},
        )
        Tile.objects.create(dashboard=dashboard, cell=cell, user=user, order=order)
        order = order - 1 if first else order + 1
        existing[query] = (None, cell)
        result[query] = remove_tile_url(cell)
    return result


def remove_tiles(user, key, connector, queries):
    """Retire les tuiles des requêtes données ; renvoie la liste des requêtes retirées."""
    existing = get_user_tiles(user, key, connector)
    removed = []
    for query in queries:
        if query not in existing:
            continue
        tile, cell = existing[query]
        tile.delete()
        if cell.placeholder == "_dashboard":
            cell.delete()
        removed.append(query)
    return removed
