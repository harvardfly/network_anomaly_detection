#!/usr/bin/python3
# -*- coding:utf-8 -*-

from django.urls import path

from messager import views

app_name = 'messager'

urlpatterns = [
    path('', views.MessagesListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('<username>/', views.ConversationListView.as_view(), name='conversation_detail'),
]
