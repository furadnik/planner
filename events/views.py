from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import EventCreateForm, UserAnswerEditForm
from .models import Event, EventUser


class EventCreateView(CreateView):
    form_class = EventCreateForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        print(self.request.user.id)
        obj.save()
        return HttpResponseRedirect(reverse("events:view", kwargs={"pk": obj.id}))


class EventDetailView(DetailView):
    model = Event


class EventEditView(UpdateView):
    form_class = EventCreateForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        print(self.request.user.id)
        obj.save()
        return HttpResponseRedirect(reverse("events:view", kwargs={"pk": obj.id}))


class FieldsEditView(UpdateView):
    form_class = EventCreateForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        print(self.request.user.id)
        obj.save()
        return HttpResponseRedirect(reverse("events:view", kwargs={"pk": obj.id}))


@require_POST
def add_user(request, pk):
    print(pk)
    event = get_object_or_404(Event, id=pk)
    name = request.POST["name"]
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    new_user = EventUser(display_name=name, event=event, user=user)
    new_user.save()
    return redirect("events:edit_answer", pk=new_user.id)


class UserAnswerEditView(UpdateView):
    form_class = UserAnswerEditForm
    template_name = "events/event_form.html"
    model = EventUser
