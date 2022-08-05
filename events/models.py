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

    def __str__(self):
        return f"{self.name} ({self.mode})"


class EventUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    display_name = models.fields.CharField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return self.event.get_absolute_url()


class Choice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ManyToManyField(EventUser)
    dt_from = models.fields.DateTimeField()
    dt_to = models.fields.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        e_type = self.event.mode

        if e_type == Modes.DTCHOICE:
            return f"{self.dt_from} -- {self.dt_to}"
        elif e_type == Modes.DATECHOICE:
            return f"{self.dt_from.date()} -- {self.dt_to.date()}"

        return str(self.dt_from.date())
