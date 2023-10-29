import re

from django import template

register = template.Library()


@register.filter
def div(arg1, arg2):
    return int(arg1 or 0) / 10 ** arg2
