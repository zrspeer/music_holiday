"""Defines URL patterns for questions app."""

from django.urls import path

from . import views

app_name = "questions"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    # Question pages
    path("q/<int:question_id>/", views.question, name="question"),
    # Questions List
    path("list/", views.question_list, name="question_list"),
    # Thank you page
    path("thank-you/", views.thank_you, name="thank_you"),
]
