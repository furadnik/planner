from django.shortcuts import reverse
from django.views.generic.edit import CreateView

from .forms import RegistrationForm


# Create your views here.
class RegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse("index")
