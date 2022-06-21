import logging

from django.template import Library, TemplateSyntaxError
from django.template.defaultfilters import stringfilter

__all__ = ["rupluralize"]

logger = logging.getLogger("django.requests")

register = Library()


@register.filter
@stringfilter
def rupluralize(value, endings):
    try:
        endings = endings.split(",")
        value = int(value)
        if value % 100 in (11, 12, 13, 14):
            return endings[2]
        if value % 10 == 1:
            return endings[0]
        if value % 10 in (2, 3, 4):
            return endings[1]
        else:
            return endings[2]
    except Exception as e:
        logger.exception(f"Error occurred at pluralizing value='{value}' endings='{endings}'")

        raise TemplateSyntaxError
