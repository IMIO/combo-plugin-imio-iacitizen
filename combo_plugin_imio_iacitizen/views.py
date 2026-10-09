import json

from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .dashboard import add_tiles, remove_tiles


@csrf_exempt
@require_POST
def dashboard_tiles(request, key):
    # en-tête impossible à poser depuis un autre site sans CORS : protège du CSRF
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return HttpResponseForbidden("missing X-Requested-With header")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("authentication required")
    if key not in settings.JSON_CELL_TYPES:
        return HttpResponseBadRequest("invalid cell type: %s" % key)
    try:
        body = json.loads(request.body)
        action = body["action"]
        connector = str(body["connector"])
        queries = [str(query) for query in body["queries"]]
    except (ValueError, KeyError, TypeError):
        return HttpResponseBadRequest("bad json request")
    if action not in ("add", "remove"):
        return HttpResponseBadRequest("invalid action: %s" % action)

    with transaction.atomic():
        if action == "add":
            tiles = add_tiles(request.user, key, connector, queries)
            if tiles is None:
                return HttpResponseNotFound("no dashboard")
            return JsonResponse({"err": 0, "tiles": tiles})
        return JsonResponse({"err": 0, "removed": remove_tiles(request.user, key, connector, queries)})
