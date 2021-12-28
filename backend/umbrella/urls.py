#/urls.py
from django.urls import include, path
from umbrella import views
from umbrella.views.lease_view import LeaseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'lease', views.LeaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
