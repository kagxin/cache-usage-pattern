#coding:utf8
'''
Created on 2017年11月14日

@author: ilinkin
'''


from django.conf.urls import url
from django.views.decorators.cache import cache_page
from app.views import TestView, ArticleListView, ArticleDetailView, CommentView

urlpatterns = [
    url(r'^article/$', ArticleListView.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetailView.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/comment/$', CommentView.as_view()),
    url(r'^test/', TestView.as_view()),
]
