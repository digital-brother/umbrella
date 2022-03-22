from django.db import transaction
from rest_framework import serializers

from umbrella.tasks.models import Task, Subtask, Comment
from umbrella.users.serializers import UserSerializer


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = [
            "title",
            "is_done",
        ]


class TaskCommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "created_by",
            "message",
            "created_at",
            "task",
        ]


class TaskSerializer(serializers.ModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "contract",
            "clause_type",
            "bl_type",
            "link_to_text",
            "title",
            "assigned_to",
            "due_date",
            "progress",
            "notes",
            "number",
            "status",
            "period",
            "when",
            "repeats",
            "until",
            "subtasks",
            "comments",
        ]

    def create(self, validated_data):
        subtasks = validated_data.pop("subtasks", [])
        task = Task.objects.create_task(**validated_data)
        for item_data in subtasks:
            Subtask.objects.create_subtask(task=task, **item_data)
        return task


class TaskUpdateSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields
        read_only_fields = ['clause_type', 'bl_type', 'link_to_text']

    @transaction.atomic
    def update(self, instance, validated_data):
        subtasks = validated_data.pop("subtasks", None)
        updated_task = Task.objects.task_update(instance, **validated_data)
        if not subtasks and not isinstance(subtasks, list):
            return updated_task

        old_checklists = Subtask.objects.filter(task=instance)
        old_checklists.delete()
        for point_data in subtasks:
            Subtask.objects.create_subtask(task=instance, **point_data)

        return updated_task
