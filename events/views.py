from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import EventCreateForm
from .models import Event


class EventCreateView(CreateView):
    form_class = EventCreateForm
    template_name = "events/date_choice_event_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        print(self.request.user.id)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class EventDetailView(DetailView):
    model = Event
