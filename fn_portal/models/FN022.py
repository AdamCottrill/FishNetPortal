from django.db import models
from django.template.defaultfilters import slugify

from .FN011 import FN011
from .BaseModel import FNPortalBaseModel


class FN022(FNPortalBaseModel):
    """
    Class to represent the seasons (temporal strata) used in each project.

    .. todo:: Add range constraints to ssn_date0 and ssn_date1 - they cannot
       overlap each other and must be contained within the project start and end
       dates (project.prj_date0 and project.prj_date1).

    .. code-block:: sql

        -- from https://dba.stackexchange.com/questions/110582/uniqueness-constraint-with-date-range
        -- the '[]' is inclusive: [1,2,3],[4,5,6] NOT [1,2,3),[3,4,5,6)
        CREATE EXTENSION btree_gist;
        ALTER TABLE fn_portal_fn022
        ADD CONSTRAINT unique_project_ssn_date0_ssn_date1
            EXCLUDE  USING gist
                ( project_id WITH =,
                daterange(ssn_date0, ssn_date1, '[]') WITH &&
            );

    """

    id = models.AutoField(primary_key=True)

    project = models.ForeignKey(
        "FN011", related_name="seasons", on_delete=models.CASCADE
    )
    ssn = models.CharField(
        help_text="Season Code", max_length=2, blank=False, db_index=True
    )
    ssn_des = models.CharField(
        help_text="Season Description", max_length=60, blank=False
    )
    ssn_date0 = models.DateField(help_text="Season Start Date", blank=False)
    ssn_date1 = models.DateField(help_text="Season End Date", blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        verbose_name = "FN022 - Season"
        ordering = ["ssn"]
        unique_together = ["project", "ssn"]

    def save(self, *args, **kwargs):
        """"""

        raw_slug = "-".join([self.project.prj_cd, self.ssn])

        self.slug = slugify(raw_slug)
        super(FN022, self).save(*args, **kwargs)

    def __str__(self):
        """return the season name, code and project code associated with this
        particular season."""

        repr = "<Season: {} ({}) [{}]>"
        return repr.format(self.ssn_des, self.ssn, self.project.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the ssn, and ssn des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.ssn_des:
            label = "{}-{}".format(self.ssn, self.ssn_des.title())
        else:
            label = "{}".format(self.ssn)
        return label
