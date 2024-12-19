from django.urls import path

from robots.views import (
    create_robot,
    robot_production_summary,
)

urlpatterns = [
    path("create/", create_robot, name="create"),
    path(
        "production-last-week/", robot_production_summary, name="production-last-week"
    ),
]
