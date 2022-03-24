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
    created_by = serializers.SerializerMethodField()
    created_at = serializers.DateField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "created_by",
            "message",
            "created_at",
            "task",
        ]

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.username

        return "Deleted"


class TaskSerializer(serializers.ModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "contract",
            "clause_type",
            "business_intelligence_type",
            "link_to_text",
            "title",
            "assignees",
            "due_date",
            "progress",
            "notes",
            "status",
            "reminder_number",
            "reminder_period",
            "reminder_before_or_after",
            "repeats",
            "until",
            "subtasks",
            "comments",
        ]

    @transaction.atomic
    def create(self, validated_data):
        subtasks = validated_data.pop("subtasks", [])
        task = Task.objects.create_task(**validated_data)
        for item_data in subtasks:
            Task.create_subtask(task, **item_data)
        return task


class TaskUpdateSerializer(TaskSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = Task.EDITABLE_FIELDS + ["subtasks", "comments"]

    @transaction.atomic
    def update(self, instance, validated_data):
        subtasks = validated_data.pop("subtasks", None)
        updated_task = Task.update(instance, **validated_data)
        replace_subtasks = subtasks or subtasks == []
        if replace_subtasks:
            old_checklists = Subtask.objects.filter(task=instance)
            old_checklists.delete()
            for item_data in subtasks:
                Task.create_subtask(instance, **item_data)

        return updated_task
