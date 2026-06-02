from django import template

register = template.Library() 

# Filter to check if a user is in a group. Form Stack Overflow as indicated on credits.
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 