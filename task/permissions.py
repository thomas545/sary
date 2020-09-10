from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Task


class StateNotDone(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.state in [Task.INPROGRESS, Task.DONE]:
            raise PermissionDenied("Can't edit task, state is done.")
        return True


class StateInProgress(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            obj.state
            and obj.state == Task.INPROGRESS
            or obj.linked_task.state == Task.INPROGRESS
        ):
            return True
        raise PermissionDenied("State isn't in progress.")
