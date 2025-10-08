# employees/templatetags/ru_pluralize.py

from django import template

register = template.Library()

@register.filter
def ru_pluralize(value, arg="сотрудник,сотрудника,сотрудников"):
    forms = arg.split(',')
    number = abs(int(value))
    if number % 10 == 1 and number % 100 != 11:
        return forms[0]
    elif number % 10 >= 2 and number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return forms[1]
    else:
        return forms[2]