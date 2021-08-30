"""
=============================================================
~/fn_portal/data_upload/target_utils.py
Created: Aug-12-2021 12:19
DESCRIPTION:

    Utility functions to connect to our target database,
    fetch lookup caches, and insert records.

A. Cottrill
=============================================================
"""


from typing import Dict, Optional, List

from django.contrib.auth import get_user_model

# from sqlalchemy import MetaData, create_engine, select

User = get_user_model()


FilterOptions = Optional[Dict[str, str]]


def get_id_cache(
    model,
    key_fields: List = [
        "slug",
    ],
    filters: FilterOptions = None,
) -> Dict:
    """Fetch a dictionary cache of unique identifiers for a django model
       and the current ID in the database.

    This function returns a dictionary containing key-value pairs that
    can be used to fetch the id of the specified model objects. Used
    to reduce the number of queries executed when data is inserted or
    updated.


    Arguments:

    - `model`: A django model class. The model must have an objects
       method with filter and values method.

    - `key_fields`: a list of field names that are to be used as the
      keys in the returned dictionary. slug by default but other
      fields are more appropriate in some cases ('spc' for species and
      'abbrev' for lakes). A

    - `filters`: The filters to be applied to queryset to reduce the
      number of records included in the cache.  Filters is a
      dictionary where the key is the django orm expression to be
      applied and the value is the value to be applied to that
      expression.

    """

    if filters:
        qs = model.objects.filter(**filters)
    else:
        qs = model.objects

    cache = {}
    for key in key_fields:
        tmp = {x[key]: x["id"] for x in qs.values(key, "id")}
        cache.update(tmp)

    return cache


def get_user_cache():
    users = User.objects.all()
    cache = {}
    for user in users:
        cache[user.username.upper()] = user.id
        firstLast = f"{user.first_name} {user.last_name}"
        cache[firstLast.upper()] = user.id
    return cache


# def get_user_cache(users):
#     """"""
#     user_cache = {}
#     for key, attrs in users.items():
#         if attrs:
#             user, created = User.objects.get_or_create(username=attrs["username"])
#             if created:
#                 for attr, value in attrs.items():
#                     setattr(user, attr, value)
#                 user.save()
#             user_cache[key.upper()] = user
#     return user_cache


# def get_user_attrs(prj_ldr):
#     """take a username from a fishnet project and return the first and
#     last name, a user address and an ontario email address."""
#     attrs = {}
#     names = prj_ldr.title().split()
#     firstName = names[0]
#     if len(names) > 1:
#         lastName = names[1]
#     else:
#         lastName = ""
#     attrs["first_name"] = firstName
#     attrs["last_name"] = lastName
#     attrs["email"] = "{}.{}@ontario.ca".format(firstName.lower(), lastName.lower())
#     attrs["username"] = lastName.lower() + firstName.lower()[:2]
#     return attrs
