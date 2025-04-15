from django import template
from dateutil.relativedelta import relativedelta
from datetime import timedelta

register = template.Library()

@register.filter
def next_month_same_day(value):
    try:
        return value + relativedelta(months=1)
    except Exception:
        return (value + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
