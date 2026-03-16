from django.urls import path
from . import views

urlpatterns = [

    path("mark-entry/", views.mark_entry, name="mark_entry"),
    path("mark-exit/", views.mark_exit, name="mark_exit"),

]