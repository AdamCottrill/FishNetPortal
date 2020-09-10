"""
=============================================================
~/fn_portal/utils.py
 Created: 09 Sep 2020 07:39:35

 DESCRIPTION:



 A. Cottrill
=============================================================
"""


def is_admin(user):
    """return true if the user belongs to the admin group, false otherwise"""
    if user.groups.filter(name="admin").exists() or user.is_superuser:
        return True
    else:
        return False
