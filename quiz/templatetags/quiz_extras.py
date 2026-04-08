# quiz/templatetags/quiz_extras.py
from django import template

register = template.Library()

@register.filter
def get_choice(question, number):
    return getattr(question, f'choice_{number}')