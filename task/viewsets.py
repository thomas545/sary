from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Task
from .permissions import StateNotDone


class TaskViewSet(viewsets.ModelViewSet):
    """
    Add new task & edit tasks
    Required fields in POST | UPDATE | PATCH: title, description
    Display fields: id, uuid, title, description, state, linked_task, created,
    """

    permission_classes = (StateNotDone,)
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    http_method_names = (
        u"get",
        u"post",
        u"put",
        u"patch",
    )
