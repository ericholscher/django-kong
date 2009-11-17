from django import template

register = template.Library()

@register.filter
def micro_to_milli(value):
    return value/1000

@register.filter
def render_twill(result):
    return result.test.render(result.site)
