#!/usr/bin/python3
# -*- coding:utf-8 -*-


import datetime

from haystack import indexes
from django.contrib.auth import get_user_model


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """对User模型类中部分字段建立索引"""
    text = indexes.CharField(
        document=True, use_template=True,
        template_name='search/users_text.txt'
    )  # users_text.txt 保存需要建立索引的字段
    # python manage.py rebuild_index 建立索引

    def get_model(self):
        return get_user_model()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            date_joined__lte=datetime.datetime.now()
        )
