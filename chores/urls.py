from django.urls import path

from . import views

app_name = "chores"

urlpatterns = [
    path("", views.health, name="health"),
    path("households/", views.households, name="households"),
]
