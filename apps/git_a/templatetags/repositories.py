from datetime import datetime
import time
import os

from django import template
register = template.Library()
 
@register.filter("repo_name")
def repo_name(value):
    return value.split(os.sep)[-1]

@register.filter("hex_sha_short")
def hex_sha_short(value):
    return "".join(list(str(value))[:8])

@register.filter("seconds_to_date")
def seconds_to_date(value):
    t = time.gmtime(value)
    return datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)