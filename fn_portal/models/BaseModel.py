from django.contrib.gis.db import models


class FNPortalBaseModel(models.Model):
    """A simple abstract model that all of our other models will inherit
    from to captuture when the record was created, and when it was
    modified.  This model could be updated at some point in the future
    to log who made the changes, but that is considereably more
    complicated as that requires access to the request object (which
    is not typically available outside of view functions).

    """

    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
