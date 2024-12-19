from django.contrib import admin
from django.urls import include, path

import robots.urls as robots_urls

urlpatterns = [
    path("robots/", include(robots_urls)),
    path("admin/", admin.site.urls),
]
