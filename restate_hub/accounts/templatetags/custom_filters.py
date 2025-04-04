from django import template

register = template.Library()

@register.filter
def get_member(user, member_type):
    """Dynamically get the related model instance based on member_type"""
    return getattr(user, member_type, None)
