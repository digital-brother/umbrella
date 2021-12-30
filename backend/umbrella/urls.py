# /urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from umbrella.views.lease_view import LeaseViewSet

router = DefaultRouter()
router.register(r"lease", LeaseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
