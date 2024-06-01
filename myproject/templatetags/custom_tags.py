from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator


register = template.Library()


@register.filter
def truncatehtml(value, arg):
    try:
        length = int(arg)
    except ValueError:  # если arg не число
        return value  # возвращаем оригинальное значение без изменений

    text_only = strip_tags(value)  # Удаление HTML тегов
    truncated_text = Truncator(text_only).chars(length)  # Обрезание до заданной длины

    if len(text_only) > length:
        return truncated_text + '...'
    return truncated_text



