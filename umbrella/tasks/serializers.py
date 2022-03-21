from django.db import transaction
from rest_framework import serializers

from umbrella.contracts.serializers import BusinessLogicModelSerializer
from umbrella.tasks.choices import StatusChoices, ProgressChoices
from umbrella.tasks.models import Task, TaskChecklist, TaskComment


class TaskChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChecklist
        fields = [
            "title",
            "is_done",
        ]


class TaskCommentSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskComment
        fields = [
            "created_by",
            "message",
            "created_by",
            "task",
        ]


# class TaskSerializer(serializers.ModelSerializer):
#     task_checklist = TaskChecklistSerializer(many=True)
#
#     class Meta:
#         model = Task
#         fields = [
#             "id",
#             "contract",
#             "task_checklist",
#             "clause_type",
#             "bl_type",
#             "link_to_text",
#             "title",
#             "assigned_to",
#             "due_date",
#             "progress",
#             "notes",
#             "number",
#             "status",
#             "period",
#             "when",
#             "repeats",
#             "until",
#         ]
#
#     def create(self, validated_data):
#         task_checklist = validated_data.pop("task_checklist")
#         obj = super().create(validated_data)
#         for item_data in task_checklist:
#             TaskChecklist.objects.create_checklist(task=obj, **item_data)
#         return obj


class TaskSerializer(BusinessLogicModelSerializer):
    task_checklist = serializers.ListField(child=serializers.DictField(), allow_empty=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "contract",
            "task_checklist",
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
        ]

    def perform_create_business_logic(self, **validated_data):
        task_checklist = self.validated_data.pop("task_checklist")
        task = Task.objects.create_task(task_checklist=task_checklist, **validated_data)
        # if not task_checklist:
        #     return task
        #
        # for item in task_checklist:
        #     item["task"] = task
        #     TaskChecklist.objects.create_checklist(**item)

        return task

    # def validate(self, attrs):
    #     task_checklist = attrs.pop("task_checklist")
    #     instance = Task(**attrs)
    #     instance.full_clean()
    #     return attrs


class TaskRetrieveSerializer(TaskSerializer):
    clause_type = serializers.CharField(read_only=True)
    bl_type = serializers.CharField(read_only=True)
    link_to_text = serializers.CharField(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields


class TaskUpdateSerializer(TaskSerializer):
    clause_type = serializers.CharField(read_only=True)
    bl_type = serializers.CharField(read_only=True)
    link_to_text = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields

    @transaction.atomic
    def update(self, instance, validated_data):
        task_checklist = validated_data.pop("task_checklist")
        if task_checklist:
            old_checklists = TaskChecklist.objects.filter(task=instance)
            old_checklists.delete()
            for point_data in task_checklist:
                TaskChecklist.objects.create_checklist(task=instance, **point_data)

        return super().update(instance, validated_data)
