from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
import django_filters

from common.models import Species

User = get_user_model()


def point_to_polygon(pt, radius_m):
    """a helper function to connect directly to postgis trasform, buffer
    and transform back our point.  The build in django functions do
    not currenly return a correctly transormed polygon (way too tall).

    """
    with connection.cursor() as cursor:
        sql = (
            """select st_transform(st_buffer(st_transform(
        st_geomfromtext(%s, 4326), 26916),%s), 4326) as poly;"""
            ""
        )
        cursor.execute(sql, [pt, radius_m])
        row = cursor.fetchone()
    return row


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class GeomFilter(django_filters.CharFilter):
    pass


class GeoFilterSet(django_filters.FilterSet):
    """A fitlerset class that includes a filter_roi method"""

    def filter_roi(self, queryset, name, value):
        """A custom filter for our region of interest, only return objects
        that have all of there sampling points in the region of interest.
        The region of interest is contained in the 'value' parameter and must be string
        that can be converted to a GEOS geometry, typically wkt or geojson.
        """

        if not value:
            return queryset
        try:
            roi = GEOSGeometry(value, srid=4326)
            geofilter = {}
            geofilter[name] = roi
            queryset = queryset.filter(**geofilter)
        except ValueError:
            pass
        return queryset

    def filter_point(self, queryset, name, value):
        """A custom filter for points.  value must be a string that can be
        converted to a geospoint objects, typically geojson or well
        known text. Optionally followed by a radius in meters to buffer the
        point by. If no radius is provided, a value of 5000 m will be
        assumed.

        POINT(-81.5 45.5);5000

        """

        if not value:
            return queryset
        try:
            if "[" in value:
                geom, radius = value.split("[")
                radius = int(radius.replace("]", ""))
            else:
                geom = value
                radius = 5000
            # get the buffered point (now a polygon from postgis) NOTE
            # - this a work-around for transform-buffer-backtransform
            # bug in django library
            polygon = point_to_polygon(geom, radius)
            roi = GEOSGeometry(polygon[0], srid=4326)

            geofilter = {}
            geofilter[name] = roi

            queryset = queryset.filter(**geofilter)
        except ValueError:
            pass
        return queryset


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
