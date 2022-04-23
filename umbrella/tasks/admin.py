from django.contrib import admin

from umbrella.tasks.models import Task, Subtask, Comment

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Comment)
