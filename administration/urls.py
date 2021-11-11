from django.conf.urls import url
from .views import (
    control_panel,
)


app_name = 'administration'



urlpatterns = [
    url(r"^control_panel$", control_panel, name="control_panel"),
]
