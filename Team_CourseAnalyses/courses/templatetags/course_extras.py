from django.template.defaultfilters import register


@register.filter
def dict_get(dict, key):
    return dict.get(key)