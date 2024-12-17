from django.urls import path

from robots.views import RobotDetailView, RobotListView, create_robot

urlpatterns = [
    path("", RobotListView.as_view(), name="robot-list"),
    path("<int:pk>/", RobotDetailView.as_view(), name="robot-detail"),
    path("create/", create_robot, name="create-robot"),
]
