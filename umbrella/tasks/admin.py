from django.contrib import admin

from umbrella.tasks.models import Task, TaskChecklist, TaskComment

admin.site.register(Task)
admin.site.register(TaskChecklist)
admin.site.register(TaskComment)
