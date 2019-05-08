from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


print('ok')
#
# {% if request.user|has_group:"mygroup" %}
#     <p>User belongs to my group
# {% else %}
#     <p>User doesn't belong to mygroup</p>
# {% endif %}