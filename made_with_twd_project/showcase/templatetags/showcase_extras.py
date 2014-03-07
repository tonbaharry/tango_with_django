__author__ = 'leif'
from django import template
from showcase.models import Category

register = template.Library()

@register.inclusion_tag("showcase/cats.html")
def get_category_list():
    return {"cats" : Category.objects.all()}
