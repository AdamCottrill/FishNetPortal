from django import template
from fn_portal.models import FN011

register = template.Library()


@register.inclusion_tag("fn_portal/_sidebar_year_projects.html")
# takes_context=True)


def sidebar_projects():
    return {"projects": FN011.objects.all().order_by("-year")}


@register.filter
def lookup(value, key):
    return value.get(key, [])


@register.simple_tag(takes_context=True)
def query_transform(context, include_page=False, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %}
    outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.

    from: https://gist.github.com/benbacardi/d6cd0fb8c85e1547c3c60f95f5b2d5e1

    if page is true, we will return the page number tag too, if it is
    false, we want to strip it out and reset our filters to page 1.
    This allows the same template tag to be used in paginators and
    'refinement' widgets.  Without, refinement widgets may point to a
    page that doesn't exist after the new filter has been applied.

    """

    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v

    if query.get("page") and not include_page:
        query.pop("page")
    return query.urlencode()


@register.simple_tag(takes_context=True)
def strip_parameter(context, param):
    """
    A template tag to remove the specified parameter from the url
    string.  If there are no parameter left, it returns the bare
    url (without any parameters or ?-mark)
    """

    query = context["request"].GET.copy()
    query.pop(param, None)

    if len(query):
        return "?" + query.urlencode()
    else:
        return context["request"].path
