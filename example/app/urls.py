#coding:utf8
'''
Created on 2017年11月14日

@author: ilinkin
'''


from django.conf.urls import url, include
from app.views import TestView, ArticleListView, ArticleDetail

urlpatterns = [
    url(r'^article/$', ArticleListView.as_view()),
    url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetail.as_view()),
    url(r'^test/', TestView.as_view()),
]
