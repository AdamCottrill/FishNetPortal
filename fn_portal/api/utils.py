"""Utilities used by our api endpoints that are not associciated with perissions."""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "page_size"
    max_page_size = 1000


class XLargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 2000


def flatten_gear(gear_array):
    """the shape of the request data from the project wizard that
    corresponds to the gears and process types are too deeply nested
    and need to be flattened to match the other data elements.  This
    function takes the deeply nested dict and flattens each one into a
    dictionary with just two elemnts: gear and proccess type.

    """
    gears = []
    for item in gear_array:
        for ptype in item.get("process_types"):
            tmp = {
                "gear": item["gear"],
                "process_type": ptype["process_type"],
            }
            gears.append(tmp)
    return gears
