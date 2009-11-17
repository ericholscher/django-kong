from django import template

register = template.Library()

def micro_to_milli(value):
    return value/1000

register.filter('micro_to_milli', micro_to_milli)
