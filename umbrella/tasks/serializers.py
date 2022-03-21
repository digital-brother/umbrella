from django.db import transaction
from rest_framework import serializers

from umbrella.contracts.serializers import BusinessLogicModelSerializer
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

    class Meta:
        model = Comment
        fields = [
            "created_by",
            "message",
            "created_by",
            "task",
        ]


# class TaskSerializer(serializers.ModelSerializer):
#     task_checklist = SubtaskSerializer(many=True)
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
#             Subtask.objects.create_checklist(task=obj, **item_data)
#         return obj


class TaskSerializer(BusinessLogicModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)

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

    def perform_create_business_logic(self, **validated_data):
        task = Task.objects.create_task(**validated_data)
        subtasks = self.initial_data.get("subtasks")
        if not subtasks:
            return task

        for item in subtasks:
            Subtask.objects.create_subtask(task=task, **item)

        return task

    # def validate(self, attrs):
    #     task_checklist = attrs.pop("task_checklist")
    #     instance = Task(**attrs)
    #     instance.full_clean()
    #     return attrs


# class TaskRetrieveSerializer(TaskSerializer):
#     comments = TaskCommentSerializer(many=True, read_only=True)
#     subtasks = SubtaskSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Task
#         fields = TaskSerializer.Meta.fields + ['comments', 'subtasks']
#         read_only_fields = ['clause_type', 'bl_type', 'link_to_text']


class TaskUpdateSerializer(BusinessLogicModelSerializer):
    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields
        read_only_fields = ['clause_type', 'bl_type', 'link_to_text']

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     subtasks = self.initial_data.get("subtasks")
    #     if subtasks:
    #         old_checklists = Subtask.objects.filter(task=instance)
    #         old_checklists.delete()
    #         for point_data in subtasks:
    #             Subtask.objects.create_subtask(task=instance, **point_data)
    #
    #     return super().update(instance, validated_data)

    def perform_update_business_logic(self, instance, **validated_data):
        task = Task.objects.task_update(instance, **validated_data)
        return task
