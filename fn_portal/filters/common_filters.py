from django.contrib.auth import get_user_model
import django_filters

from common.models import Species

User = get_user_model()


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class SpeciesFilter(django_filters.FilterSet):

    spc = ValueInFilter(field_name="spc")
    spc__not = ValueInFilter(field_name="spc", exclude=True)

    spc_nmco__like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains"
    )

    spc_nmsc__like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains"
    )

    spc_nmco__not_like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains", exclude=True
    )

    spc_nmsc__not_like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = Species
        fields = ["spc", "spc_nmco", "spc_nmsc"]


class UserFilter(django_filters.FilterSet):
    """A filter class for user objects. Case insentitive filter for
    username, first name and lastname.  Also exposes filters to return
    users who are currently active, and those who are staff."""

    username__like = django_filters.CharFilter(
        field_name="username", lookup_expr="icontains"
    )

    first_name__like = django_filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )

    last_name__like = django_filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )

    username = django_filters.CharFilter(field_name="username", lookup_expr="iexact")

    first_name = django_filters.CharFilter(
        field_name="first_name", lookup_expr="iexact"
    )

    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="iexact")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
