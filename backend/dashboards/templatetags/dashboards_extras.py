import datetime
import json
import re

from django import template

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def div(arg1, arg2):
    return int(arg1 or 0) / 10 ** arg2


@register.filter
def bar_color(value):
    if isinstance(value, (int, float)):
        if value > 80:
            return "bg-success"
        elif value > 60:
            return "bg-primary"
        elif value > 40:
            return "bg-info"
        elif value > 20:
            return "bg-warning"
        else:
            return "bg-danger"


@register.filter(name='json_to_dict')
def json_to_dict(value):
    return json.loads(value)


@register.filter(name='layer_badge')
def layer_badge(layers):
    css = 'bg-label-warning' if layers == '3' else "bg-label-info"
    return f'<span class="badge {css}">{layers}-сл</span>'


@register.filter
def month_name(month_number):
    if not month_number:
        month_number = 0
    return [
        datetime.date.today().year,
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    ][int(month_number)]


@register.filter
def format_name(customer):
    start = customer.name.upper().index(customer.name_stripped)
    end = start + len(customer.name_stripped)
    return f'<strong>{customer.name[start:end]}</strong> <span class="text-light fw-semibold">{customer.name[:start].strip("«»“")}' \
           f'</span><span class="text-muted">{customer.name[end:].rstrip(""""« »“""")}</span>'


@register.filter
def number_plate(string):
    try:
        segment = list(re.findall(r'([A-ZАВЕКМНОРСТУХ]+)(\d+)([A-ZАВЕКМНОРСТУХ]+)(\d+)', string)[0])
        return f"""
        <div class="plate">
            <div class="plate-number">
                <div class="plate-letters">{segment[0]}</div>
                <div class="number">{segment[1]}</div>
                <div class="plate-letters">{segment[2]}</div>
            </div>
            <div class="plate-region">
                {segment[3]}<div class="code">rus</div>
            </div>
        </div>
        """
    except BaseException:
        return f'<div class="plate"><div class="plate-number">{string}</div></div>'
