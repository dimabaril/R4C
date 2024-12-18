from django.urls import path

from robots.views import (
    RobotDetailView,
    RobotListView,
    create_robot,
    robot_production_summary,
)

urlpatterns = [
    path("", RobotListView.as_view(), name="list"),
    path("<int:pk>/", RobotDetailView.as_view(), name="detail"),
    path("create/", create_robot, name="create"),
    path(
        "production-last-week/", robot_production_summary, name="production-last-week"
    ),
]
