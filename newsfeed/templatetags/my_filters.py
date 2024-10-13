from django.template import Library
from django.utils import timezone

register = Library()

@register.filter
def utc(value, arg):
    tz = timezone.get_default_timezone()
    return value.astimezone(tz)