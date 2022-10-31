from django.db import models

from .Gear import Gear
from .FN011 import FN011


from .BaseModel import FNPortalBaseModel


class ProjectGearProcessType(FNPortalBaseModel):
    """
    ProjectGearProcessType holds the process types for each gear as
    specified in the design of the project.  The processtype captures
    how the catch in each net is recorded and directly influences the
    number of FN122 records associated with each net set.
    """

    PROCESS_TYPE_CHOICES = [
        ("1", "By Sample"),
        ("2", "By Mesh Size"),
        ("3", "By Panel Group"),
        ("4", "By Panel"),
        ("5", "Other (TBD)"),
    ]

    id = models.AutoField(primary_key=True)

    project = models.ForeignKey(
        FN011, related_name="gear_process_types", on_delete=models.CASCADE
    )

    gear = models.ForeignKey(
        Gear, related_name="project_process_types", on_delete=models.CASCADE
    )

    process_type = models.CharField(
        "Process type choice associated with this gear.",
        default="1",
        choices=PROCESS_TYPE_CHOICES,
        max_length=2,
    )

    class Meta:
        unique_together = ["project", "gear", "process_type"]

    def __str__(self):
        return "{}-{}-{}".format(
            self.project.prj_cd, self.gear.gr_code, self.process_type
        )
