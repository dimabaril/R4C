import datetime
import json
from http import HTTPMethod, HTTPStatus

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from robots.forms import RobotForm
from robots.utils import generate_robot_production_summary


@csrf_exempt
@require_http_methods([HTTPMethod.POST])
def create_robot(request):
    try:
        data = json.loads(request.body)
        form = RobotForm(data)

        if form.is_valid():
            robot = form.save(commit=False)
            serial = f'{data["model"]}-{data["version"]}'
            robot.serial = serial
            robot.save()
            return JsonResponse(
                {"status": "success", "message": "Robot created successfully!"},
                status=HTTPStatus.CREATED,
            )

        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=HTTPStatus.BAD_REQUEST
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON format"},
            status=HTTPStatus.BAD_REQUEST,
        )


@require_http_methods(["GET"])
def robot_production_summary(request):

    to_time = datetime.datetime.now()
    from_time = to_time - datetime.timedelta(
        days=settings.ROBOT_PRODUCTION_SUMMARY_DAYS
    )

    workbook = generate_robot_production_summary(from_time, to_time)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="robots_production_since_{from_time}_to_{to_time}.xlsx"'
    )

    # Save workbook to response
    workbook.save(response)

    return response
