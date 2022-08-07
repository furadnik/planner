from django.urls import path

from .views import (ChoicesView, EventCreateView, EventDetailView,
                    EventEditView, UserAnswerEditView, add_user)

app_name = "events"
urlpatterns = [
    path("create", EventCreateView.as_view(), name="create"),
    path("<str:pk>/view", EventDetailView.as_view(), name="view"),
    path("<str:pk>/edit", EventEditView.as_view(), name="edit"),
    path("<str:pk>/choices", ChoicesView.as_view(), name="choices"),
    path("<str:pk>/add_user", add_user, name="user"),
    path("<str:pk>/edit_answer", UserAnswerEditView.as_view(), name="answer"),
]
