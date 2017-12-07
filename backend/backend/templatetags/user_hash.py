from django import template
register = template.Library()

@register.filter(name='get_user_hash')
def get_user_hash(value):
    return abs(hash(hash(value)))
