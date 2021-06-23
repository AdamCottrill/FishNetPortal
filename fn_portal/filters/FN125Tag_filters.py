import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN125Tag

from .FishAttr_filters import FishAttrFilters


class FN125TagFilter(FishAttrFilters):
    """A fitlerset that allows us to select subsets of tag objects by
    by attributes of the tag (fn125 tag data only)"""

    tagid = ValueInFilter(field_name="tagid")
    tagid__like = ValueInFilter(field_name="tagid")
    tagid__not_like = ValueInFilter(field_name="tagid", exclude=True)

    tagdoc = ValueInFilter(field_name="tagdoc")
    tagdoc__like = ValueInFilter(field_name="tagdoc")
    tagdoc__not_like = ValueInFilter(field_name="tagdoc", exclude=True)

    tagstat = ValueInFilter(field_name="tagstat")
    tagstat__not = ValueInFilter(field_name="tagstat", exclude=True)

    # consider splitting up tagdoc into consitiuent fields to make it
    # easier to filter by colour, placement tag type and agency.

    class Meta:
        model = FN125Tag
        fields = ["tagstat", "tagid", "tagdoc"]
