from django.shortcuts import render
from django.views import generic

from courses.models import Course


class IndexView(generic.ListView):
    template_name = 'courses/index.html'

    def get_queryset(self):
        return Course.objects.all()