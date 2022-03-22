from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from umbrella.contracts.models import Lease
from umbrella.tasks.choices import (
    ProgressChoices,
    RepeatsChoices,
    PeriodChoices,
    WhenChoices,
)

User = get_user_model()


class SubtaskManager(models.Manager):
    def create_subtask(self, task, **data):
        checklist = self.model(task=task, **data)
        checklist.full_clean()
        checklist.save()

        return checklist


class TaskManager(models.Manager):
    def create_task(self, **data):
        assigned_to = data.pop("assigned_to", [])
        task = self.model(**data)
        task.full_clean()
        task.save()
        task.assigned_to.set(assigned_to)

        return task

    def task_update(self, task, **kwargs):
        allowed_attributes = {
            "title",
            "assigned_to",
            "due_date",
            "progress",
            "notes",
            "number",
            "period",
            "when",
            "repeats",
            "until",
        }
        for name, value in kwargs.items():
            assert name in allowed_attributes
            setattr(task, name, value)

        task.full_clean()
        task.save()
        return task


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


def now_and_due_date_diff(task):
    due_date = task.due_date
    today = date.today()
    date_dif = due_date - today
    return date_dif.days


def two_days_ahead():
    return date.today() + timedelta(days=2)


class Task(models.Model):
    # Common data
    title = models.CharField(max_length=500, validators=[MinLengthValidator(5)])
    assigned_to = models.ManyToManyField(User, related_name="executors", blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.CharField(
        max_length=32,
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
    )
    notes = models.TextField(null=True, blank=True)

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

    objects = TaskManager()

    class Meta:
        ordering = ["-created_at"]

    @property
    def status(self):
        if not self.due_date:
            return "Overdue"
        elif not self.due_date and self.progress == ProgressChoices.COMPLETED:
            return "Done"

        date_diff = now_and_due_date_diff(self)
        if date_diff < 0 and self.progress == ProgressChoices.COMPLETED:
            return "Done"
        elif date_diff < 0:
            return "Overdue"
        elif date_diff == 0:
            return "Due Today"
        elif date_diff <= 7:
            return "Due in a Week"
        elif date_diff <= 31:
            return "Due in a Month"
        elif date_diff > 31:
            return "Not Due Soon"


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)

    objects = SubtaskManager()


class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
