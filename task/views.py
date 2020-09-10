from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError

from .serializers import (
    TaskSerializer,
    DisplayTasksSerializer,
    LinkedTasksTogetherSerializer,
    ChangeTaskState,
    LinkedTwoTasksSerialzer,
)
from .models import Task
from .permissions import StateInProgress


class LinkTwoTasksView(generics.CreateAPIView):
    permission_classes = (StateInProgress,)
    serializer_class = LinkedTwoTasksSerialzer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_1 = get_object_or_404(
            Task, pk=int(serializer.validated_data.get("task_one"))
        )
        task_2 = get_object_or_404(
            Task, pk=int(serializer.validated_data.get("task_two"))
        )
        task_1.linked_task = task_2
        task_2.linked_task = task_1
        task_1.save()
        task_2.save()
        return Response({"detail": "tasks were linked successfully!"})


class LinkTaskView(generics.RetrieveUpdateAPIView):
    """
    Display linked tasks with any id/pk,
    Linked two tasks together

    Endpoint = linked/tasks/current_task_id/

    GET -> Fields: id, uuid, title, description, state, linked_task, created
    UPDATE | PATCH -> Fields: {linked_task: another_task_id}

    response -> tasks linked successfully!
    """

    permission_classes = (StateInProgress,)
    serializer_class = DisplayTasksSerializer
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.linked_task:
            raise NotAcceptable("Task already linked")

        serializer = LinkedTasksTogetherSerializer(
            instance=task, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Task.objects.filter(id=request.data.get("linked_task")).update(linked_task=task)

        return Response({"detail": "tasks linked successfully!"})


class RemoveLinkedTaskView(views.APIView):
    """
    Remove link between tasks
    Endpoint: remove/linked/task_id/

    response: Linked removed successfully.
    """

    def get_object(self):
        pk = self.kwargs.get("pk")
        instance = get_object_or_404(Task, pk=pk)
        return instance

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        linked = task.linked_task
        if not task.linked_task or not linked.linked_task:
            raise ValidationError("No linked to remove.")
        linked.linked_task = None
        task.linked_task = None
        linked.save()
        task.save()

        return Response({"detail": "Linked removed successfully."})


class ChangeTaskStateView(generics.RetrieveUpdateAPIView):
    """
    Change Task state
    Endpoint: change-state/task_id/
    state :
    - n = New
    - i = In Progress
    - d = Done

    request: {"state": "i"}
    response: {"state": "d", "state_value": "Done"}
    """

    serializer_class = ChangeTaskState
    queryset = Task.objects.all()
