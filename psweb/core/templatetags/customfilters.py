from django import template

register = template.Library()

@register.filter(name='lookup')
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except Exception as e:
        return None