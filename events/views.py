from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import (ChoiceForm, DCForm, DRForm, DTCForm, EventForm,
                    UserAnswerForm)
from .models import Choice, Event, EventUser


# EVENT {{{
class EventsIndexView(ListView):
    model = Event
    paginate = 30
    template_name = "index.html"


class EventCreateView(CreateView):
    form_class = EventForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        print(self.request.user.id)
        obj.save()
        return HttpResponseRedirect(reverse("events:view", kwargs={"pk": obj.id}))


class EventDetailView(DetailView):
    model = Event


class EventEditView(LoginRequiredMixin, UpdateView):
    form_class = EventForm
    template_name = "events/event_edit_form.html"
    model = Event

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.creator != self.request.user:
            raise PermissionDenied()
        return obj

# }}}


MODES_CHOICES_FORMS = {
    "DR": DRForm,
    "DC": DCForm,
    "DTC": DTCForm
}


class ChoicesView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    form_class = ChoiceForm
    template_name = "events/choices.html"
    model = Choice

    def test_func(self):
        return self.request.user == self.event.creator

    def get_event(self, pk):
        self.event = get_object_or_404(Event, id=pk)
        try:
            self.form_class = MODES_CHOICES_FORMS[self.event.mode]
        except KeyError:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        self.get_event(pk)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "_method" in request.POST.keys() and request.POST["_method"] == "delete":
            return self.delete(request, *args, **kwargs)
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_return_url())

    def delete(self, request, *args, **kwargs):
        self.success_url = self.event.get_absolute_url()
        choice = get_object_or_404(
            Choice, id=request.POST["choice_id"], event=self.event
        )
        choice.delete()

    def get_return_url(self):
        if self.event.choices_single_editable:
            return reverse("events:choices", kwargs={"pk": self.event.id})
        return self.event.get_absolute_url()

    def form_valid(self, form):
        form.save_with_event(self.event.id)
        return HttpResponseRedirect(self.event.get_absolute_url())

# ADD USER {{{


@require_POST
def add_user(request, pk):
    event = get_object_or_404(Event, id=pk)
    name = request.POST["name"]
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    new_user = EventUser(display_name=name, event=event, user=user)
    new_user.save()
    return redirect("events:answer", pk=new_user.id)


class UserAnswerEditView(UpdateView):
    form_class = UserAnswerForm
    template_name = "events/answer.html"
    model = EventUser
# }}}
