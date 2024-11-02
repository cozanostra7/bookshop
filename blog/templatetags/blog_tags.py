from django import template
from blog.models import Category,Favourite

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_favourite(article,user):
    return Favourite.objects.filter(article = article,user=user).exists()
