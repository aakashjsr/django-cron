"""
Copyright (c) 2007-2008, Dj Gilcrease
All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from django.db import models
try:
    from django.utils import timezone
    now = timezone.now
except ImportError:
    # Django<=1.3 compatibility
    from datetime import datetime
    now = datetime.now


class Job(models.Model):
    
    name = models.CharField(max_length=100)
    
    # Time between job runs (in minutes) // default: 1 day
    run_frequency = models.PositiveIntegerField(default=1440)
    last_run = models.DateTimeField(default=timezone.now, null=True)
    
    instance = models.TextField()
    args = models.TextField()
    kwargs = models.TextField()
    queued = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def debug(self):
        from django_cron.base import pickle_loads_and_decode
        inst = pickle_loads_and_decode(str(self.instance))
        args = pickle_loads_and_decode(str(self.args))
        kwargs = pickle_loads_and_decode(str(self.kwargs))
        inst.run(*args, **kwargs)
        self.last_run = now()
        self.save()


class Cron(models.Model):
    executing = models.BooleanField(default=False)