import inflect
from django import template

register = template.Library()

p = inflect.engine()

@register.filter(name='number_to_words')
def number_to_words(value):
    """Converts an integer into words."""
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value
    return p.number_to_words(value)
