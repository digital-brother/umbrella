from django.urls import path

from umbrella.notifications.views import SendNotificationView

urlpatterns = [
    path('notifications/send/', SendNotificationView.as_view(), name='send_notification')
]
