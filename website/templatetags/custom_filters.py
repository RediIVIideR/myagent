from django import template

register = template.Library()


@register.filter
def split_by_character(value, arg):
    return value.split(arg)
