from django.db import transaction
from rest_framework import serializers

from umbrella.core.serializers import CustomWritableNestedModelSerializer, CustomModelSerializer
from umbrella.tasks.models import Task, Subtask, Comment


class SubtaskSerializer(CustomModelSerializer):
    class Meta:
        model = Subtask
        fields = [
            "title",
            "is_done",
        ]


class TaskCommentSerializer(CustomModelSerializer):
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


class TaskSerializer(CustomWritableNestedModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, required=False)
    contract_file_name = serializers.CharField(source="contract.file_name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "contract",
            "contract_file_name",
            "contract_clause_type",
            "contract_business_intelligence_type",
            "link_to_contract_text",
            "title",
            "assignees",
            "due_date",
            "progress",
            "notes",
            "status",
            "reminder_number",
            "reminder_period",
            "reminder_before_or_after",
            "reminder_repeats",
            "reminder_until",
            "subtasks",
            "comments",
        ]


class TaskUpdateSerializer(TaskSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = Task.EDITABLE_FIELDS + ["subtasks", "comments"]

    @transaction.atomic
    def update(self, instance, validated_data):
        subtasks = validated_data.pop("subtasks", None)
        updated_task = super().update(instance, validated_data)

        replace_subtasks = subtasks or subtasks == []
        if replace_subtasks:
            old_subtasks = Subtask.objects.filter(task=instance)
            old_subtasks.delete()
            for item_data in subtasks:
                updated_task.create_subtask(**item_data)

        return updated_task
