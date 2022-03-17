from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models, transaction

from umbrella.contracts.models import Lease
from umbrella.tasks.choices import ProgressChoices, RepeatsChoices, PeriodChoices, \
    WhenChoices, StatusChoices

User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def set_status_if_due_date(task):
    due_date = task.due_date
    today = date.today()
    date_dif = due_date - today
    progress = task.progress
    status = status_from_date_dif(date_dif.days, progress)
    return status


def status_from_date_dif(date_dif, progress):
    if date_dif < 0 and progress == ProgressChoices.COMPLETED:
        return StatusChoices.DONE
    elif date_dif < 0:
        return StatusChoices.OVERDUE
    elif date_dif == 0:
        return StatusChoices.DUE_TODAY
    elif date_dif <= 7:
        return StatusChoices.DUE_IN_A_WEEK
    elif date_dif <= 31:
        return StatusChoices.DUE_IN_A_MONTH
    elif date_dif > 31:
        return StatusChoices.NOT_DUE_SOON


def two_days_ahead():
    return date.today() + timedelta(days=2)


class Task(models.Model):
    # Common data
    title = models.CharField(max_length=128)
    assigned_to = models.ManyToManyField(User, related_name="executors", blank=True)
    due_date = models.DateField(null=True, blank=True)
    progress = models.CharField(
        max_length=32, choices=ProgressChoices.choices, default=ProgressChoices.NOT_STARTED
    )
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=32, choices=StatusChoices.choices, default=StatusChoices.DONE
    )

    # Contract info
    contract = models.ForeignKey(Lease, on_delete=models.CASCADE)
    clause_type = models.CharField(max_length=128)
    bl_type = models.CharField(max_length=128)
    link_to_text = models.CharField(max_length=1024)

    # Reminder
    number = models.PositiveIntegerField(default=1)
    period = models.CharField(
        max_length=32, choices=PeriodChoices.choices, default=PeriodChoices.DAYS
    )
    when = models.CharField(
        max_length=32, choices=WhenChoices.choices, default=WhenChoices.BEFORE
    )
    repeats = models.CharField(
        max_length=32, choices=RepeatsChoices.choices, default=RepeatsChoices.NEVER
    )
    until = models.DateField(null=True, blank=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_created = not self.pk
        if is_created:
            status = set_status_if_due_date(self)
            self.status = status
        super().save(*args, **kwargs)


class TaskChecklist(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_checklist")
    title = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)


class TaskComment(models.Model):
    message = models.CharField(max_length=1024)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
