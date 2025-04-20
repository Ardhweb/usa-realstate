from django import template

register = template.Library()

@register.simple_tag
def get_member_field(user, field_name, default_value=''):
    try:
        related_obj = getattr(user, user.member_type, None)
        if related_obj:
            return getattr(related_obj, field_name, default_value)
        else:
            return default_value
    except Exception:
        return default_value
