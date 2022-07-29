from django import template
register = template.Library()

@register.filter(name='get_dict_val')
def get_dict_val(d,key):
    if type(d)==list:
        return d[key]
    return d.get(key)