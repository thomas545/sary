from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Task
from ..views import LinkTasksView, RemoveLinkedTaskView, ChangeTaskStateView
from ..viewsets import TaskViewSet


class SetupTestMainViews(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="test task",
            description="test task model",
        )
        self.linked = Task.objects.create(
            title="test linked task", description="test linked task model"
        )


class TestViewSetsCases(SetupTestMainViews):
    def test_task_view_post(self):
        url = reverse("task-list")
        data = {"title": "task testing", "description": "task description test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_view_edit(self):
        url = reverse("task-detail", kwargs={"pk": self.task.pk})
        data = {
            "title": "task updating title",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), data.get("title"))

    def test_task_view_state_done(self):
        url = reverse("task-detail", kwargs={"pk": self.task.pk})
        self.task.state = Task.DONE
        self.task.save()
        data = {
            "title": "task updating title",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), "Can't edit task, state is done.")


class TestViewsCases(SetupTestMainViews):
    def test_link_tasks(self):
        url = reverse("link_tasks", kwargs={"pk": self.task.pk})
        data = {"linked_task": self.linked.id}
        self.task.state = Task.INPROGRESS
        self.task.save()

        response = self.client.put(url, data)
        self.assertEqual(response.data.get("detail"), "tasks linked successfully!")

    def test_linked_tasks(self):
        url = reverse("link_tasks", kwargs={"pk": self.task.pk})
        data = {"linked_task": self.linked.id}
        self.task.state = Task.INPROGRESS
        self.task.linked_task = self.linked
        self.task.save()

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data.get("detail"), "Task already linked")

    def test_alredy_removed_linked_tasks(self):
        url = reverse("remove_linked", kwargs={"pk": self.task.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "No linked to remove.")

    def test_remove_linked_tasks(self):
        self.task.state = Task.INPROGRESS
        self.task.linked_task = self.linked
        self.task.save()
        self.linked.linked_task = self.task
        self.linked.save()
        url = reverse("remove_linked", kwargs={"pk": self.task.pk})

        response = self.client.post(url)
        self.assertEqual(response.data.get("detail"), "Linked removed successfully.")

    def test_chage_task_status(self):
        url = reverse("change_state", kwargs={"pk": self.task.pk})
        data = {"state": "d"}

        response = self.client.put(url, data)
        self.assertEqual(response.data.get("state"), "d")
        self.assertEqual(response.data.get("state_value"), "Done")
