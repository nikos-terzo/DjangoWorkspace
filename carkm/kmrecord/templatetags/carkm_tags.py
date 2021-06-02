from django import template

register = template.Library()

@register.simple_tag
def set(val):
	print(val)
	print(type(val))
	return val