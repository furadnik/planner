"""Event's models."""
import uuid
from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class Modes(models.TextChoices):
    """Event modes."""

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

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.fields.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.fields.CharField(max_length=30, choices=modes)

    @property
    def max_number_of_participants(self) -> Optional[int]:
        """Get the maximum number of users at a choice."""
        return len(max(self.choice_set.all(), key=lambda x: len(x.user.all())).user.all())

    @property
    def choices_single_editable(self) -> bool:
        """Whether or not the choices are signle editable by the user."""
        return not self.mode == str(Modes.DATERANGE)

    def get_absolute_url(self):
        """Absolute url of the model."""
        return reverse("events:view", kwargs={"pk": self.id})

    def __str__(self):  # pragma: no cover
        """Represent an event."""
        return f"{self.name} ({self.mode})"

    def get_date_range(self):
        """Get date range of event's choices."""
        choices = self.choice_set.all()
        if len(choices) == 0:
            return None, None

        first = min(choices, key=lambda x: x.dt_from)
        last = max(choices, key=lambda x: x.dt_to)
        return first.dt_from, last.dt_to

    def set_date_range(self, dt_from, dt_to):
        """Trim choices outside of the specified range."""
        for choice in self.choice_set.all():
            if choice.dt_from < dt_from or choice.dt_to > dt_to:
                Choice.delete(choice)

    class Meta:
        """Set ordering."""

        ordering = ['-created_at']


class EventUser(models.Model):
    """A model combining the event and the user models."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    display_name = models.fields.CharField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        """Represent the EU."""
        return self.display_name

    def get_absolute_url(self):  # pragma: no cover
        """Absolute url of the model."""
        return self.event.get_absolute_url()


class Choice(models.Model):
    """An event's choice for the users."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ManyToManyField(EventUser)
    dt_from = models.fields.DateTimeField()
    dt_to = models.fields.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        """Represent the Choice."""
        e_type = self.event.mode

        if e_type == Modes.DTCHOICE:
            return f"{self.dt_from} -- {self.dt_to}"
        elif e_type == Modes.DATECHOICE:
            return f"{self.dt_from.date()} - {self.dt_to.date()}"

        return str(self.dt_from.date())

    @property
    def color(self) -> str:
        """Get color of choice cell."""
        max_participants = self.event.max_number_of_participants
        if not max_participants:
            return "#ffffff"

        max_color = 255
        user_ratio = len(self.user.all()) / max_participants
        my_color = int(max_color * (1 - user_ratio))
        return f"rgb({my_color}, 255, {my_color})"
