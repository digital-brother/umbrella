from django.db import transaction
from rest_framework import serializers

from umbrella.tasks.choices import StatusChoices
from umbrella.tasks.models import Task, TaskChecklist, TaskComment


class TaskChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChecklist
        fields = [
            'title',
            'is_done',
        ]


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment


class TaskSerializer(serializers.ModelSerializer):
    task_checklist = TaskChecklistSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'contract',
            'task_checklist',
            'clause_type',
            'bl_type',
            'link_to_text',
            'title',
            'assigned_to',
            'due_date',
            'progress',
            'notes',
            'number',
            'status',
            'period',
            'when',
            'repeats',
            'until',
        ]

    def create(self, validated_data):
        task_checklist = validated_data.pop('task_checklist')
        obj = super().create(validated_data)
        for point_data in task_checklist:
            TaskChecklist.objects.create(task=obj, **point_data)
        return obj


class TaskUpdateSerializer(TaskSerializer):
    clause_type = serializers.CharField(read_only=True)
    bl_type = serializers.CharField(read_only=True)
    link_to_text = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields

    @transaction.atomic
    def update(self, instance, validated_data):
        progress = validated_data.get("progress")
        task_checklist = validated_data.pop('task_checklist')
        if task_checklist:
            old_checklists = TaskChecklist.objects.filter(task=instance)
            old_checklists.delete()
            for point_data in task_checklist:
                TaskChecklist.objects.create(task=instance, **point_data)

        if progress and instance.status == StatusChoices.OVERDUE:
            instance.status = StatusChoices.DONE

        return super().update(instance, validated_data)

