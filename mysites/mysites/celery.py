# -*- coding:utf-8 -*-
 
from __future__ import absolute_import,unicode_literals  # 注意此项必须放在最上方, 为了向上版本兼容
 
import os
 
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysites.settings')

 
app = Celery('mysites')
 

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#这步暂时还不懂在做什么
@app.task(bind=True)
def test(self):
    print('Request:{0!r}'.format(self.request))
