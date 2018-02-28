from datetime import date, datetime
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from courses.models import Course


class IndexView(generic.ListView):
    template_name = 'courses/index.html'

    def get_queryset(self):
        return Course.objects.all()


def index(request):
    course_list = Course.objects.all()
    show_time, ongoing_course_list = get_show_time(course_list)
    recommend_course_list = Course.objects.filter(course_id='95880')

    return render(request, 'courses/index.html',
                  {'course_list': course_list, 'ongoing_course_list': ongoing_course_list, 'show_time': show_time,
                   'recommend_course_list': recommend_course_list})


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

    recommend_course_list = Course.objects.filter(course_id='95880')
    if course_list:
        show_time, ongoing_course_list = get_show_time(course_list)
    else:
        show_time, ongoing_course_list = get_show_time(recommend_course_list)

    return render(request, 'courses/index.html',
                  {'course_list': course_list, 'ongoing_course_list': ongoing_course_list, 'search_field': search_field,
                   'show_time': show_time, 'recommend_course_list': recommend_course_list})


def get_show_time(course_list):
    show_time = {}
    current_course_list = []

    now = datetime.now()
    day = now.strftime('%A')[0]
    time = now.strftime('%H:%M')
    now_minutes = int(time[0:2]) * 60 + int(time[3:5])

    for course in course_list:
        if 'A' not in course.section or '4' in course.section or day not in course.days:  # not a current course
            if course.days == 'TBA':
                show_time[course.pk] = course.days
            else:
                show_time[course.pk] = course.days + ' ' + course.begin
        else:
            beg_minutes = get_course_minutes(course.begin)
            end_minutes = get_course_minutes(course.end)

            if now_minutes < beg_minutes < now_minutes + 60:
                show_time[course.pk] = 'Starts in %d minutes' % (beg_minutes - now_minutes)
                current_course_list.append(course)
            elif beg_minutes < now_minutes < end_minutes:
                show_time[course.pk] = 'Ends in %d minutes' % (end_minutes - now_minutes)
                current_course_list.append(course)
            else:
                show_time[course.pk] = course.days + course.begin

    return show_time, current_course_list


def get_course_minutes(time):
    hour = int(time[0:2])
    minute = int(time[3:5])

    if time[5:7] == 'PM' and hour != 12:
        hour += 12

    return hour * 60 + minute
