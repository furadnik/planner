"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (EventCreateView, EventDetailView, EventEditView,
                    FieldsEditView, UserAnswerEditView, add_user)

app_name = "events"
urlpatterns = [
    path("create", EventCreateView.as_view(), name="create"),
    path('view/<str:pk>/', EventDetailView.as_view(), name="view"),
    path('edit/<str:pk>/', EventEditView.as_view(), name="edit"),
    path('fields/<str:pk>/', FieldsEditView.as_view(), name="fields"),
    path('add_user/<str:pk>/', add_user, name="edit_answer_user_add"),
    path('edit_answer/<str:pk>', UserAnswerEditView.as_view(), name="edit_answer"),
]
