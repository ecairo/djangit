import time
import os
from datetime import datetime
from django import template
register = template.Library()

from ..utils import normalize_size as normalize


@register.filter("repo_name")
def repo_name(value):
    return value.split(os.sep)[-1]


@register.filter("hex_sha_short")
def hex_sha_short(value):
    return "".join(list(str(value))[:8])


@register.filter("seconds_to_date")
def seconds_to_date(value):
    t = time.localtime(value)
    return datetime(t.tm_year, t.tm_mon, t.tm_mday,
                    t.tm_hour, t.tm_min, t.tm_sec)


@register.filter("avatar")
def gravatar_avatar(value):
    return 'http://www.gravatar.com/avatar/%s?s=100&d=404' % value


@register.filter("normalize_size")
def normalize_size(value):
    return normalize(int(value))
