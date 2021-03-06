# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings
from celery import Celery

app = Celery('exodus', backend='amqp://', include=['exodus.core.apk','exodus.core.dns','exodus.core.http'], broker=settings.CELERY_BROKER_URL)

if __name__ == '__main__':
    app.start()