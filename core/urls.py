from django.conf.urls import url, include
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^atividade1/$', views.atividade1, name='atividade1'),
    url(r'^atividade2/$', views.atividade2, name='atividade2'),
    url(r'^atividade2-csv/$', views.atividade2_csv, name='atividade2_csv'),
    url(r'^atividade3/$', views.atividade3, name='atividade3'),
    url(r'^atividade4/$', views.atividade4, name='atividade4'),
    url(r'^atividade5/$', views.atividade5, name='atividade5'),
    url(r'^atividade5-csv/$', views.atividade5_csv, name='atividade5_csv')

]
