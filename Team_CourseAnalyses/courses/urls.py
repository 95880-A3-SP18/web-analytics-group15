from django.urls import path

from courses import views

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('statistic/', views.statistic, name='statistic')
]