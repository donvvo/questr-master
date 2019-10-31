from django.conf.urls import patterns, include, url
from django.conf import settings

import views as mainview
import quests.views as questviews
import users.views as userviews
# from api import views as apiview

# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^$', mainview.index, name="index"),
    url(r'^contactus/$', mainview.contactus, name='contactus'),
    url(r'^signup/invitation/', userviews.signup_by_invitation, name='signup_by_invitation'),
    url(r'^user/', include('users.urls')),
    url(r'^quest/', include('quests.urls') ),
    url(r'^api/v1/', include('api.urls') ),
    url(r'^track/', questviews.tracking_number_search, name='trackquest'),
    url(r'^contact/', mainview.contact, name='contact' ),
    url(r'^news/', mainview.news, name='news' ),
    url(r'^company/join/', mainview.join, name='join' ),
    url(r'^company/about/', mainview.about, name='about' ),
    url(r'^terms/', mainview.terms, name='terms' ),
    url(r'^privacy/', mainview.privacy, name='privacy' ),    
    url(r'^team/', mainview.team, name='team' ),    
    url(r'^career/', mainview.career, name='career' ),    
    url(r'^help/faq/', mainview.faq, name='faq' ),
    url(r'^help/crowdshipping/', mainview.crowdshipping, name='crowdshipping' ),
    url(r'^help/trust/', mainview.trust, name='trust' ),
    url(r'^apply/', include('application.urls')),
    url(r'^about/', mainview.about, name='about' ),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^loadpage/(?P<template>[-_\w/.]+)$', mainview.loadPage, ),
    )
