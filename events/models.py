import uuid

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from model_utils.managers import InheritanceManager


class Modes(models.TextChoices):
    DATERANGE = "DR"
    DATECHOICE = "DC"
    DTCHOICE = "DTC"


class Event(models.Model):
    """Represents an event."""
    modes = (
        (Modes.DATERANGE, "Date Range"),
        (Modes.DATECHOICE, "Date Choice"),
        (Modes.DTCHOICE, "Date-Time Choice")
    )

    objects = InheritanceManager()
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.fields.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.fields.CharField(max_length=30, choices=modes)

    def get_absolute_url(self):
        return reverse("events:view", kwargs={"pk": self.id})


class EventUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    display_name = models.fields.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Choice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    dt_from = models.fields.DateTimeField()
    dt_to = models.fields.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
