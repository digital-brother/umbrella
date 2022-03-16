from django.db import models


class ProgressChoices(models.TextChoices):
    NOT_STARTED = 'NOT_STARTED', 'Not Started'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'


class RepeatsChoices(models.TextChoices):
    NEVER = 'NEVER', 'Not Never'
    EVERYDAY = 'EVERYDAY', 'Everyday'
    EVERY_WEEK = 'EVERY_WEEK', 'Every week'
    EVERY_MONTH = 'EVERY_MONTH', 'Every month'


class PeriodChoices(models.TextChoices):
    DAYS = 'DAYS', 'Days'
    WEEKS = 'WEEKS', 'Weeks'
    MONTHS = 'MONTHS', 'Months'


class WhenChoices(models.TextChoices):
    BEFORE = 'BEFORE', 'Before'
    AFTER = 'AFTER', 'After'


# class StatusChoices(models.TextChoices):
#     NEVER = 'NEVER', 'Not Never'
#     EVERYDAY = 'EVERYDAY', 'Everyday'
#     EVERY_WEEK = 'EVERY_WEEK', 'Every week'
#     EVERY_MONTH = 'EVERY_MONTH', 'Every month'
