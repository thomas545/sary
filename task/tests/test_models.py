from rest_framework.test import APITestCase
from ..models import Task


class TestModelCases(APITestCase):
    def test_task(self):
        task = Task.objects.create(title="test task", description="test task model")
        self.assertEqual(task.__str__(), task.title)
