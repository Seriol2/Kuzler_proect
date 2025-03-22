from django.urls import path

from .views import LessonView


app_name = "lessons"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('lessons/', LessonView.as_view()),
]