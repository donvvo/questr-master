from django.conf.urls import patterns, url

import views as questviews

urlpatterns = patterns('',
    url(r'^$', questviews.viewDeliveries, name='viewDeliveries'),
    url(r'^new/$', questviews.newquest, name='newquest'),
    url(r'^confirm/$', questviews.confirmquest, name='confirmquest'),
    url(r'^getdistanceandprice/$', questviews.getDistanceAndPrice, name='getdistanceandprice'),    
    url(r'^activequests/$', questviews.viewallactivequests, name='activequests'),    
    url(r'^allquests/$', questviews.viewallquests, name='allquests'),    
    url(r'^pastquests/$', questviews.viewallpastquests, name='pastquests'),    
    url(r'^accept/(?P<quest_code>[\w\d]+)', questviews.accept_quest, name='accept_quest'),
    url(r'^reject/(?P<quest_code>[\w\d]+)', questviews.reject_quest, name='reject_quest'),
    url(r'^(?P<questname>[\w\d]+)/$', questviews.viewquest, name='viewquest'),
    url(r'(?P<questname>[\w\d]+)/complete/(?P<deliverycode>[\w\d]+)', questviews.completequest, name='completequest'),
)
