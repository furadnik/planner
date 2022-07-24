from django import forms

from .models import Event


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["creator"]
