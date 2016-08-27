# -*- coding: utf-8 -*-
"""lawyerFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.home , name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^lawyerHome/(?P<law_id>\d{2,10})$', views.lawyerHome, name='lawyer_home'),
    url(r'^lawyerHome/mypage/(?P<law_id>\d{2,10})$', views.lawyerHomeMyPage, name='lawyer_home_mypage'),
    
    url(r'^undercons/$', views.undercons, name='undercons'),
    url(r'^ckeditor/$', include('ckeditor_uploader.urls')),
    #url(r'^site_service_rule', TemplateView.as_view(template_name='common/site_service_rule.html'),name='service_rule'),
    url(r'^site_service_rule', views.service_rule, name='service_rule'),

    
    url(r'^tmp/$', views.tmp, name='tmp'),
    
    # for TTD
    url(r'^home_page/$', views.home_page, name='home_page'),
    url(r'^lists/the-only-list-in-the-world/$', views.view_list, name='view_list'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    