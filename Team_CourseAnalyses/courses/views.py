from datetime import date, datetime
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

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
            if course.begin != 'TBA' and course.end != 'TBA':
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
            else:
                show_time[course.pk] = course.days + ' ' + course.begin + ' ' + course.end
                # Yunlu: there might have situations where course.begin or course.end are 'TBA'
                # so it could not change to int

    return show_time, current_course_list


def get_course_minutes(time):
    hour = int(time[0:2])
    minute = int(time[3:5])

    if time[5:7] == 'PM' and hour != 12:
        hour += 12

    return hour * 60 + minute


def statistic(request):
    search = request.GET.get('search_pre')
    if search == 'please enter a course id' or search is None:
        return render (request, 'courses/statistic.html')
    elif not search.isdigit():
        return render(request, 'courses/statistic.html', {'error_message': 'ONLY ALLOW DIGITS >>> eg. 9 or 95 or 95880'})
    else:
        cor_draw, pre_draw = saveSpecificRelation(search)
        return render(request, 'courses/statistic.html', {'search_pre': search, 'cor_draw':cor_draw, 'pre_draw':pre_draw})


def saveSpecificRelation(search):
    picpath = '{}/courses/static/courses/images/'.format(os.getcwd())
    filepath = '../parser/course_detail_csv/Spring_2018_description.csv'

    course_df = pd.read_csv(filepath)
    prerequisites_df = course_df[course_df.Prerequisites != 'None'][['Course_id', 'Prerequisites']]
    corequisites_df = course_df[course_df.Corequisites != 'None'][['Course_id', 'Corequisites']]

    cor_G = nx.Graph()
    cor_draw = False
    for index in range(len(corequisites_df)):
        course = corequisites_df.iloc[index]['Course_id']
        cor = corequisites_df.iloc[index]['Corequisites']
        if search in str(course):
            try:
                for item in cor.split():
                    if item != ',':
                        cor_draw = True
                        cor_G.add_edge(course, item)
            except:
                pass

    if os.path.exists('{}cor_specific.png'.format(picpath)):
        os.remove('{}cor_specific.png'.format(picpath))
    if cor_draw == True:
        plt.figure(3, figsize=(8, 8))
        nx.draw(cor_G, with_labels=True, node_color='lightskyblue', edge_color='blue', node_size=80, alpha=0.8)
        plt.savefig("{}cor_specific.png".format(picpath))
        plt.close()

    pre_G = nx.DiGraph()
    pre_draw = False
    for index in range(len(prerequisites_df)):
        course = prerequisites_df.iloc[index]['Course_id']
        pre = prerequisites_df.iloc[index]['Prerequisites']
        if search in str(course):
            try:
                for pre_course in pre.replace("(", " ").replace(")", " ").replace("and", " ").replace("or", " ").split():
                    pre_draw = True
                    pre_G.add_edge(pre_course, course)
            except:
                pass

    if os.path.exists('{}pre_specific.png'.format(picpath)):
        os.remove('{}pre_specific.png'.format(picpath))
    if pre_draw == True:
        plt.figure(3, figsize=(12, 12))
        nx.draw(pre_G, with_labels=True, node_color='lightskyblue', edge_color='blue', node_size=80, alpha=0.8)
        plt.savefig("{}pre_specific.png".format(picpath))
        plt.close()

    return (cor_draw, pre_draw)