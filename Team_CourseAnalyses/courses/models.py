from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=5)
    course_title = models.CharField(max_length=100)
    session = models.CharField(max_length=50)
    units = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    mini = models.CharField(max_length=10)
    days = models.CharField(max_length=10)
    begin = models.CharField(max_length=10)
    end = models.CharField(max_length=10)
    teaching_location = models.CharField(max_length=50)
    bldg_room = models.CharField(max_length=50)
    instructor = models.CharField(max_length=50)

    def __str__(self):
        return self.course_title
