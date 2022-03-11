from django.urls import path

from umbrella.contracts.views import AddFileView

urlpatterns = [
    path('add-file/', AddFileView.as_view(), name='add_file'),
]