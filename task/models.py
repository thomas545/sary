import uuid
from django.db import models
from django.utils.translation import ugettext as _u
from django_fsm import FSMField, transition


class Task(models.Model):
    NEW = "n"
    INPROGRESS = "i"
    DONE = "d"

    STATE_CHOICES = (
        (NEW, _u("New")),
        (INPROGRESS, _u("In Progress")),
        (DONE, _u("Done")),
    )

    uuid = models.UUIDField(
        db_index=True, unique=True, editable=False, default=uuid.uuid4
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    state = FSMField(max_length=1, choices=STATE_CHOICES, default=NEW)
    linked_task = models.OneToOneField(
        "self", related_name="linked", on_delete=models.SET_NULL, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @transition(field=state, source=NEW, target=INPROGRESS)
    def in_progress(self):
        return "in progress"

    @transition(field=state, source=INPROGRESS, target=DONE)
    def done(self):
        return "Done"
