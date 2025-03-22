from django.db import models

class Lesson(models.Model):
    discipline = models.CharField(max_length=240)
    time = models.CharField(max_length=20)
    teachername = models.CharField(max_length=120)
    numclassroom = models.IntegerField()

    def __str__(self):
        return self.discipline