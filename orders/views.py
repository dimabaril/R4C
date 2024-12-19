import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        form = OrderForm(data)

        if form.is_valid():
            customer_email = form.cleaned_data["customer_email"]
            model = form.cleaned_data["model"]
            version = form.cleaned_data["version"]

            customer, _created = Customer.objects.get_or_create(email=customer_email)
            robot_serial = f"{model}-{version}"

            Order.objects.create(customer=customer, robot_serial=robot_serial)

            return JsonResponse(
                {"status": "success", "message": "Order created successfully!"},
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
