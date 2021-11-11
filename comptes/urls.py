from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import random, string
from .views import (
    index,
    profile,
    changer_profile,
    test,
    profile,
    ActivateAccount,
    verification_message,
    remove_user,
)



app_name = "comptes"



def generate_random():
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_lowercase  + string.digits) for _ in range(64))


urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^test$", test, name="test"),
    url(r"^verification$", verification_message, name="verification_message"),
    url(r"^profile/(?P<id>[0-9a-zA-Z]*)$", profile, name="profile"),
    url(r"^profile/(?P<id>[0-9a-zA-Z]*)/edit$", changer_profile, name="changer_profile"),
    url(r"^deconnexion$", LogoutView.as_view(next_page="/"), name="deconnexion"),
    url(r"^remove_user$", remove_user, name="remove_user"),
    path(f"activation/{generate_random()}", verification_message, name="verification_message"),
    path("activer/<uidb64>/<token>/", ActivateAccount.as_view(), name="activer"),
]
