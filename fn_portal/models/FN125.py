from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN123 import FN123


class FN125(FNPortalBaseModel):
    """
    A table for biological data collected from fish
    """

    id = models.AutoField(primary_key=True)

    catch = models.ForeignKey(FN123, related_name="fish", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    fish = models.CharField("Fish Id", max_length=6)
    flen = models.IntegerField("Fork Length(mm)", blank=True, null=True)
    tlen = models.IntegerField("Total Length(mm)", blank=True, null=True)
    rwt = models.FloatField("Round Weight (g)", blank=True, null=True)
    eviswt = models.FloatField("Eviscerated Weight(g)", blank=True, null=True)
    girth = models.IntegerField("Girth (mm)", blank=True, null=True)
    clipa = models.CharField("Clips applied", max_length=20, blank=True, null=True)
    clipc = models.CharField("Clips on capture", max_length=20, blank=True, null=True)
    sex = models.CharField(
        "A code identifying the sex of a fish.",
        max_length=2,
        blank=True,
        null=True,
        db_index=True,
    )
    mat = models.CharField(
        "Maturity", max_length=2, blank=True, null=True, db_index=True
    )
    gon = models.CharField(
        "Gonad Condition", max_length=4, blank=True, null=True, db_index=True
    )
    gonwt = models.FloatField("Gonad Weigth (g)", blank=True, null=True)
    noda = models.CharField("Nodules applied", max_length=20, blank=True, null=True)
    nodc = models.CharField(
        "Nodules present on caputure", max_length=20, blank=True, null=True
    )

    stom_contents_wt = models.FloatField(
        "Stomach contents weight (g)", blank=True, null=True
    )

    tissue = models.CharField("Tissues Sampled", max_length=20, blank=True, null=True)
    agest = models.CharField(
        "Age Structures Sampled", max_length=20, blank=True, null=True
    )
    fate = models.CharField("Fish Fate Code", max_length=2, blank=True, null=True)

    STOM_FLAG_CHOICES = (
        ("0", "Not Collected"),
        ("1", "FN126 Records"),
        ("2", "External Database"),
    )
    stom_flag = models.CharField(
        help_text="Was a stomach sample collected?",
        max_length=1,
        default=0,
        choices=STOM_FLAG_CHOICES,
    )

    comment5 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["catch", "fish"]
        unique_together = ("catch", "fish")

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.catch, self.fish)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125, self).save(*args, **kwargs)
