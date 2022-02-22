from django.db import models
from markdown import markdown


class FNProtocol(models.Model):
    """
    A table to capture the assessment protocols available for
    projects.

    The description field provides more detailed information in
    markdown that is converted to html when the object is saved.

    active and confirmed boolean fields capture if the protocol is
    active being used (and will be presented as an option in the
    project setup forms), and whether or not it has been documented
    (confirmed).

    An admin interface has been created for this model.

    """

    label = models.CharField(max_length=100, unique=True)
    abbrev = models.CharField(max_length=10, unique=True)
    description = models.TextField(
        "Protocol Description in markdown", blank=True, null=True
    )
    description_html = models.TextField("Protocol Description", blank=True, null=True)
    # has this gear been confirmed - accurate and correct.
    confirmed = models.BooleanField("Has this protocol been documented?", default=False)
    active = models.BooleanField("Is this protocol currently in use?", default=False)

    def __str__(self):
        return "{} ({})".format(self.label, self.abbrev)

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description)
        super(FNProtocol, self).save(*args, **kwargs)
