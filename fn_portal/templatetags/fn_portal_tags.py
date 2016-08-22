from django import template
from fn_portal.models import FN011

register = template.Library()

@register.inclusion_tag('fn_portal/_sidebar_year_projects.html')
                        #takes_context=True)

def sidebar_projects():
    return {'projects': FN011.objects.all().order_by('-year')}
