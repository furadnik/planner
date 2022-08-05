from django import forms

from .models import Choice, Event, EventUser


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class EventCreateForm(forms.ModelForm):  # {{{
    class Meta:
        model = Event
        exclude = ["creator"]

# }}}


class EventFieldsForm(forms.Form):  # {{{
    class Meta:
        model = Event

# }}}


class DRFieldsForm(EventFieldsForm):  # {{{
    start = DatePickerInput()
    end = DatePickerInput()

# }}}


class DCFieldsForm(EventFieldsForm):  # {{{
    start = DatePickerInput()
    end = DatePickerInput()

# }}}


class DTCFieldsForm(EventFieldsForm):  # {{{
    start = DateTimePickerInput()
    end = DateTimePickerInput()
# }}}


class UserAnswerEditForm(forms.ModelForm):  # {{{
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

        return instance  # }}}
