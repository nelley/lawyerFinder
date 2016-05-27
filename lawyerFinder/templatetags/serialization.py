from django import template


register = template.Library()

@register.filter(name='get_string')
def get_string(list):
    result = ", ".join(x for x in list)
    return result