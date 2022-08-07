from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = "accounts"
urlpatterns = [
    # path("register/", EventCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
]
