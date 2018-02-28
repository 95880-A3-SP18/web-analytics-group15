from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from courses.models import Course


class IndexView(generic.ListView):
    template_name = 'courses/index.html'

    def get_queryset(self):
        return Course.objects.all()


def search(request):
    search_field = request.GET.get('search_field')
    search_word = request.GET.get('search_word')

    if search_field == 'all':
        course_list = Course.objects.filter(Q(course_id=search_word) |
                                            Q(course_title__contains=search_word) |
                                            Q(bldg_room__contains=search_word) |
                                            Q(instructor__contains=search_word))
    elif search_field == 'title':
        course_list = Course.objects.filter(course_title__contains=search_word)
    elif search_field == 'instructor':
        course_list = Course.objects.filter(instructor__contains=search_word)
    elif search_field == 'building':
        course_list = Course.objects.filter(bldg_room__contains=search_word)

    return render(request, 'courses/index.html', {'course_list': course_list, 'search_field': search_field})