#!/usr/bin/python3
# -*- coding:utf-8 -*-

from django.urls import path

from notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationUnreadListView.as_view(), name='unread'),
    path('mark-as-read/<slug>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_read'),
    path('latest-notifications/', views.get_latest_notifications, name='latest_notifications'),
]
