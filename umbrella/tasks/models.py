from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models

from umbrella.contracts.models import Lease
from umbrella.tasks.choices import ProgressChoices, RepeatsChoices, PeriodChoices, \
    WhenChoices

User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def two_days_ahead():
    return date.today() + timedelta(days=2)


class Task(models.Model):
    # Contract info
    contract = models.ForeignKey(Lease, on_delete=models.CASCADE)
    clause_type = models.CharField(max_length=128)
    bl_type = models.CharField(max_length=128)
    link_to_text = models.CharField(max_length=1024)

    title = models.CharField(max_length=128)
    assigned_to = models.ManyToManyField(User, related_name="executors")
    due_date = models.DateField(null=True, blank=True)
    progress = models.CharField(
        max_length=32, choices=ProgressChoices.choices, default=ProgressChoices.NOT_STARTED
    )
    notes = models.TextField(null=True, blank=True)
    # status = models.CharField(
    #     max_length=32, choices=RepeatsChoices.choices, default=RepeatsChoices.EVERYDAY
    # )

    # Reminder
    number = models.PositiveIntegerField()
    period = models.CharField(
        max_length=32, choices=PeriodChoices.choices, default=PeriodChoices.DAYS
    )
    when = models.CharField(
        max_length=32, choices=WhenChoices.choices, default=WhenChoices.BEFORE
    )
    repeats = models.CharField(
        max_length=32, choices=RepeatsChoices.choices, default=RepeatsChoices.EVERYDAY
    )
    until = models.DateField(null=True, blank=True)


class TaskChecklist(models.Model):
    title = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskComment(models.Model):
    message = models.CharField(max_length=1024)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
