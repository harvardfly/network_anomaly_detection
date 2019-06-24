#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import os
import sys
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings_local")
django.setup()
application = get_default_application()
