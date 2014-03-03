__author__ = 'leif'

from django.conf.urls import patterns, url
from showcase import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))