"""Utilities used by our api endpoints that are not associciated with perissions."""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 2000


class XLargeResultsSetPagination(PageNumberPagination):
    page_size = 2000
    page_size_query_param = "page_size"
    max_page_size = 5000


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


def check_distinct_seasons(data):
    """A little helper function to check that seasons do not overlap -
    return true if the values are disticnt(valid) and do not
    overlap. returns false if the season are not distict and share
    some dates.
    """

    if len(data) <= 1:
        return True

    # pull out the dates, but only look a records with both start and end date
    dates = [
        (x.get("ssn_date0"), x.get("ssn_date1"))
        for x in data
        if x.get("ssn_date0") and x.get("ssn_date1")
    ]
    dates.sort()

    for i, x in enumerate(dates[:-1]):
        if x[1] >= dates[i + 1][0]:
            return False
    return True
