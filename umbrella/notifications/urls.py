from django.urls import path

from umbrella.notifications.views import NotificationsListView

urlpatterns = [
    path('list/', NotificationsListView.as_view(), name='notifications-list')
]