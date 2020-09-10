from rest_framework import serializers
from .models import Task


class LinkedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "uuid",
            "title",
            "description",
            "state",
            "linked_task",
            "created",
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "uuid",
            "title",
            "description",
            "state",
            "linked_task",
            "created",
        )
        read_only_fields = (
            "id",
            "uuid",
            "state",
            "linked_task",
            "created",
        )
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
        }


class DisplayTasksSerializer(serializers.ModelSerializer):
    linked_task = LinkedTaskSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = (
            "id",
            "uuid",
            "title",
            "description",
            "state",
            "linked_task",
            "created",
        )
        read_only_fields = (
            "id",
            "uuid",
            "title",
            "description",
            "state",
            "linked_task",
            "created",
        )


class LinkedTasksTogetherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("linked_task",)


class ChangeTaskState(serializers.ModelSerializer):
    state_value = serializers.SerializerMethodField(required=False, read_only=True)

    def get_state_value(self, obj):
        return obj.get_state_display()

    class Meta:
        model = Task
        fields = (
            "state",
            "state_value",
        )
