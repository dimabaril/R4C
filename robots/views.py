import json
from http import HTTPMethod, HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from robots.forms import RobotForm
from robots.models import Robot


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


class RobotListView(ListView):
    model = Robot
    template_name = "robots/robots_list.html"
    context_object_name = "robots"


class RobotDetailView(DetailView):
    model = Robot
    template_name = "robots/robot_detail.html"
    context_object_name = "robot"
