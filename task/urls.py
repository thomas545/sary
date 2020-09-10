from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views, viewsets


router = routers.DefaultRouter()

router.register("task", viewsets.TaskViewSet, basename='task')

urlpatterns = [
    path("", include(router.urls)),
    path("linked/tasks/<int:pk>/", views.LinkTasksView.as_view(), name="link_tasks"),
    path(
        "remove/linked/<int:pk>/",
        views.RemoveLinkedTaskView.as_view(),
        name="remove_linked",
    ),
    path(
        "change-state/<int:pk>/",
        views.ChangeTaskStateView.as_view(),
        name="change_state",
    ),
]
