from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django_fsm import can_proceed

from .models import Task


class StateNotDone(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.state in [Task.INPROGRESS, Task.DONE]:
            raise PermissionDenied("Can't edit task, state is done.")
        return True


class StateInProgress(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not can_proceed(obj.in_progress) or not can_proceed(
            obj.linked_task.in_progress
        ):
            return True
        raise PermissionDenied("State isn't in progress.")
