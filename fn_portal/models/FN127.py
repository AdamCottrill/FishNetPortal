from django.contrib.gis.db import models
from django.utils.text import slugify
from django.db.models import Q, UniqueConstraint

from .FN125 import FN125
from .BaseModel import FNPortalBaseModel


class FN127(FNPortalBaseModel):
    """
    A table for age interpretations collected from fish
    """

    id = models.AutoField(primary_key=True)

    fish = models.ForeignKey(
        FN125, related_name="age_estimates", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    ageid = models.IntegerField("An identifier for an age estimate record")
    agea = models.IntegerField(
        "Age Assessed (yr)", blank=True, null=True, db_index=True
    )
    preferred = models.BooleanField(
        "Preferred age estimate for a fish", default=False, db_index=True
    )
    agest = models.CharField(
        "Age Structure", max_length=5, db_index=True, blank=True, null=True
    )
    xagem = models.CharField("Age Assigned Method", max_length=2, blank=True, null=True)
    agemt = models.CharField("Age Method Data", max_length=5)
    edge = models.CharField("Edge Code", max_length=2, blank=True, null=True)
    conf = models.IntegerField("Confidence", blank=True, null=True)
    nca = models.IntegerField("Number of Complete Annuli", blank=True, null=True)

    agestrm = models.IntegerField("Fish Stream Age (yr)", blank=True, null=True)
    agelake = models.IntegerField("Fish Lake Age (yr)", blank=True, null=True)
    spawnchkcnt = models.IntegerField(
        "The number of observed spawning checks", blank=True, null=True
    )

    AGE_FAIL_CHOICES = [
        ("91", "No structure*"),
        ("92", "Regenerated Scale / Crystalized Otolith"),
        ("93", "Poorly Prepared Structure (poor rolled slide, cracked, sliced etc.)"),
        ("94", "Mixed structures / unreliable contaminated sample"),
        ("95", "Poor structure / unable to determine reliable age"),
    ]

    age_fail = models.CharField(
        "reason for aging attemp failure",
        choices=AGE_FAIL_CHOICES,
        max_length=2,
        blank=True,
        null=True,
    )

    ageaDate = models.DateTimeField(blank=True, null=True)

    comment7 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "ageid"]
        unique_together = ("fish", "ageid")
        indexes = [
            models.Index(fields=["fish", "preferred"]),
            models.Index(fields=["fish", "ageid", "preferred"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=["fish"],
                name="idx_fish_one_preferred_age",
                condition=Q(preferred=True),
            ),
        ]

    def __str__(self):
        return "{} (age={})".format(self.slug.upper(), self.agea)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN127, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.ageid)
