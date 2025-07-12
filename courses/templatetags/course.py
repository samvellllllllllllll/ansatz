from django import template

register=template.Library()

@register.filter
def model_name(obj):
    # d={'text':'Текст', 'image':'Изображение', 'video': 'Видео', 'file':'Файл'}
    try:
        return obj._meta.model_name
    except AttributeError:
        return None