from django.urls import re_path

import django_cron.admin_views

urlpatterns = [
    re_path(r'^restart/$', django_cron.admin_views.restart),
]
