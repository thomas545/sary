from rest_framework.test import APITestCase
from ..models import Task
from ..serializers import (
    LinkedTaskSerializer,
    TaskSerializer,
    DisplayTasksSerializer,
    LinkedTasksTogetherSerializer,
    ChangeTaskState,
)


class TestSerializersCases(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="test task", description="test task model"
        )

    def test_linked_task_serializer(self):
        serializer = LinkedTaskSerializer(instance=self.task)
        self.assertEqual(serializer.data.get("id"), self.task.id)
        self.assertEqual(serializer.data.get("title"), self.task.title)
        self.assertEqual(serializer.data.get("description"), self.task.description)

    def test_task_serializer_post(self):
        data = {"title": "task testing", "description": "task description test"}
        serializer = TaskSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)

    def test_task_serializer_get(self):
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data.get("id"), self.task.id)
        self.assertEqual(serializer.data.get("title"), self.task.title)

    def test_display_tasks_serializer(self):
        linked = Task.objects.create(
            title="test linked task", description="test linked task model"
        )
        self.task.linked_task = linked
        self.task.save()
        linked.linked_task = self.task
        linked.save()

        serializer = DisplayTasksSerializer(instance=self.task)
        self.assertEqual(serializer.data.get("linked_task").get("id"), linked.id)

    def test_linked_tasks_together_serializer(self):
        linked = Task.objects.create(
            title="test linked task", description="test linked task model"
        )
        data = {"linked_task": linked.id}
        serializer = LinkedTasksTogetherSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)

    def test_change_task_state(self):
        data = {"state": "n"}
        serializer = ChangeTaskState(data=data)
        self.assertEqual(serializer.is_valid(), True)