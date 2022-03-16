from rest_framework import serializers

from umbrella.tasks.models import Task, TaskChecklist, TaskComment


class TaskChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChecklist


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'contract',
            'clause_type',
            'bl_type',
            'link_to_text',
            'title',
            'assigned_to',
            'due_date',
            'progress',
            'notes',
            'number',
            'period',
            'when',
            'repeats',
            'until',
        ]
