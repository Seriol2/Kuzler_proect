from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lesson


class LessonView(APIView):
    def get(self, request):
        lessons = Lesson.objects.all()
        return Response({"lessons": lessons})
