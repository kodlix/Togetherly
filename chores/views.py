import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse

from .models import Household, Membership


def health(request):
    return JsonResponse({"status": "ok"})


def _request_data(request):
    if request.content_type == "application/json":
        try:
            return json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return None
    return request.POST


@login_required
def households(request):
    if request.method == "GET":
        memberships = Membership.objects.filter(user=request.user).select_related(
            "household"
        )
        return JsonResponse(
            {
                "households": [
                    {
                        "id": membership.household_id,
                        "name": membership.household.name,
                        "archived": membership.household.archived,
                        "role": membership.role,
                    }
                    for membership in memberships
                ]
            }
        )

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed."}, status=405)

    data = _request_data(request)
    name = data.get("name", "").strip() if data is not None else ""
    if not name:
        return JsonResponse({"error": "A household name is required."}, status=400)

    with transaction.atomic():
        household = Household.objects.create(name=name)
        Membership.objects.create(
            user=request.user,
            household=household,
            role=Membership.Role.OWNER,
        )

    return JsonResponse(
        {
            "id": household.id,
            "name": household.name,
            "archived": household.archived,
            "role": Membership.Role.OWNER,
        },
        status=201,
    )
