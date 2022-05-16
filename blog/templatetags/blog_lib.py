from django import template

register = template.Library()


@register.filter(name="range")
def range_filter(value, arg="1"):
    return range(int(arg), int(value))
