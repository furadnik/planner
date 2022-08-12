import datetime

from django import forms
from django.shortcuts import get_object_or_404

from .models import Choice, Event, EventUser


# DATE, DATETIME INPUT {{{
class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'
# }}}


class EventForm(forms.ModelForm):  # {{{
    class Meta:
        model = Event
        exclude = ["creator"]
# }}}


# Choices forms {{{
class ChoiceForm(forms.ModelForm):

    def save_with_event(self, id):
        obj = self.save(commit=False)
        obj.event_id = id
        obj.save()
        return obj

    class Meta:
        model = Choice
        fields = ["dt_from", "dt_to"]


class DCForm(ChoiceForm):
    """Choice form for date choice mode."""
    class Meta(ChoiceForm.Meta):
        widgets = {
            'dt_from': DatePickerInput(),
            'dt_to': DatePickerInput()
        }


class DTCForm(ChoiceForm):
    """Choice form for date choice mode."""
    class Meta(ChoiceForm.Meta):
        widgets = {
            'dt_from': DateTimePickerInput(),
            'dt_to': DateTimePickerInput()
        }


class DRForm(DCForm):
    """Choice form for date choice mode."""
    class Meta(ChoiceForm.Meta):
        widgets = {
            'dt_from': DatePickerInput(),
            'dt_to': DatePickerInput()
        }

    def save_with_event(self, id):
        event = get_object_or_404(Event, id=id)

        dt_from, dt_to = self.cleaned_data["dt_from"].replace(), self.cleaned_data["dt_to"].replace()

        event.set_date_range(dt_from, dt_to)
        curr_dt_from, curr_dt_to = event.get_date_range()
        if curr_dt_from is None:
            curr_dt_from = dt_to + datetime.timedelta(days=1)
            curr_dt_to = curr_dt_from

        date = dt_from
        while date < curr_dt_from:
            Choice(event=event, dt_from=date, dt_to=date).save()
            date += datetime.timedelta(days=1)

        date = curr_dt_to
        while date < dt_to:
            date += datetime.timedelta(days=1)
            Choice(event=event, dt_from=date, dt_to=date).save()
# }}}


class UserAnswerForm(forms.ModelForm):  # {{{
    choice_set = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Choice.objects.none(),
        required=False
    )

    class Meta:
        model = EventUser
        fields = ["choice_set"]

    def __init__(self, *args, **kargs):
        super(forms.ModelForm, self).__init__(*args, **kargs)
        self.fields['choice_set'].queryset = Choice.objects.filter(event=self.instance.event.id)
        self.fields["choice_set"].initial = self.instance.choice_set.all()

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        # Explicitly save the altered choice set.
        instance.choice_set.set(self.cleaned_data['choice_set'])

        return instance
# }}}
