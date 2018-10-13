# -*- coding: utf-8 -*-
import os
import sys
from django.core.wsgi import get_wsgi_application

local_path = sys.path[0]
sys.path.append(os.path.join(local_path, '../'))  # NoQA
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings_local'
application = get_wsgi_application()

from nt_resource.utils import insert_cat_data  # NoQA

insert_cat_data.delay(1538331058000, 1539934343000)
