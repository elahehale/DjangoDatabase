import json

from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import io
from django.views.decorators.http import require_GET
from .models import PlayLog
from django.http import Http404

KEYS = [
    "final_score",
    "rewards",
    "time",
    "spikes_removed",
    "pause_time",
    "moves",
    "win",
]

@csrf_exempt
def submit_log(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # Save the whole payload as-is
    data = PlayLog.objects.create(payload=data)
    return JsonResponse({"status": "ok", "id": data.id})

@csrf_exempt
def get_by_id(request, id):
    try:
        log = PlayLog.objects.get(pk=id)
    except PlayLog.DoesNotExist:
        raise Http404("Log does not exist")

    data = {
        "id": log.id,
        "created_at": log.created_at,
        "payload": log.payload,
    }
    return JsonResponse({"status": "ok", "data": data})


@require_GET
def export_logs_csv(request):
    qs = PlayLog.objects.all()

    all_keys = set()
    rows = []
    for obj in qs.only("id", "payload"):
        payload = obj.payload or {}
        rows.append((obj.id, payload))
        all_keys.update(payload.keys())

    fieldnames = ["id"] + sorted(all_keys)

    buff = io.StringIO()
    writer = csv.DictWriter(buff, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for _id, payload in rows:
        row = {"id": _id}
        for k in all_keys:
            row[k] = payload.get(k, "")
        writer.writerow(row)

    resp = HttpResponse(buff.getvalue(), content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="playlogs.csv"'
    return resp