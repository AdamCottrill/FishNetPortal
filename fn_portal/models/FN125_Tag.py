from django.contrib.gis.db import models

from django.template.defaultfilters import slugify


from .FN125 import FN125

# NOTE - this should be named FN125_Tag
class FN125Tag(models.Model):
    """
    A table for the tag(s) assoicated with a fish.
    """

    id = models.AutoField(primary_key=True)

    fish = models.ForeignKey(FN125, related_name="fishtags", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    fish_tag_id = models.IntegerField("Identifier for a Fn125_tag record")
    # tag fields
    tagstat = models.CharField(
        "Tag Status", max_length=5, db_index=True, blank=True, null=True
    )
    tagid = models.CharField(
        "Tag Identification", max_length=20, db_index=True, blank=True, null=True
    )
    tagdoc = models.CharField(
        "Tag Documentation", max_length=6, db_index=True, blank=True, null=True
    )
    xcwtseq = models.CharField(
        "Sequential CWT number", max_length=5, blank=True, null=True
    )
    xtaginckd = models.CharField(max_length=6, blank=True, null=True)
    xtag_chk = models.CharField(max_length=50, blank=True, null=True)

    comment_tag = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "fish_tag_id"]
        unique_together = ("fish", "fish_tag_id")

    def __str__(self):
        return "{} ({} ({}))".format(self.slug.upper(), self.tagid, self.tagdoc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125Tag, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.fish_tag_id)
