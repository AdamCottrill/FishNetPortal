from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .BaseModel import FNPortalBaseModel
from .FN122 import FN122


class FN122ElectroFishing(FNPortalBaseModel):
    """A table to hold information about electrofishing settings and
    effort - volts, amps, waveform, total seconds. ect. Associated
    with a specific elecro fishing FN122 record. Modeled as an
    optional 1:1 record.

    """

    id = models.AutoField(primary_key=True)

    effort = models.OneToOneField(
        FN122,
        related_name="electro_fishing_data",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    shock_sec = models.IntegerField(
        "A measure of shocking effort, measured in seconds.",
        blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    volts_minimum = models.FloatField(
            blank=True, null=True,
        validators=[MinValueValidator(0)])

    volts_maximum = models.FloatField(            blank=True, null=True,validators=[MinValueValidator(0)])
    volts_mean = models.FloatField(            blank=True, null=True,validators=[MinValueValidator(0)])

    amps_minimum = models.FloatField(
        "Minimum current observed a sample or transect.",
                    blank=True, null=True,
        validators=[MinValueValidator(0)],
    )
    amps_maximum = models.FloatField(
        "Maximum current observed a sample or transect.",
                    blank=True, null=True,
        validators=[MinValueValidator(0)],
    )
    amps_mean = models.FloatField(
        "Mean current observed a sample or transect.",
            blank=True, null=True,
        validators=[MinValueValidator(0)]
    )

    power_minimum = models.FloatField(
        "Minimum power output during an electrofishing sample.",
            blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    power_maximum = models.FloatField(
        "Maximum power output during an electrofishing sample.",
                    blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    power_mean = models.FloatField(
        "Maximum power output during an electrofishing sample.",
        blank=True, null=True,
        validators=[MinValueValidator(0)])

    conduct = models.FloatField(
        "Measured conductivity of the water in microsiemens (microS).",
        blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    turbidity = models.FloatField(
        "Measured turbidity of the water within a sample, measured in NTU:",
        blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    turbid_cat = models.FloatField(validators=[MinValueValidator(0)])

    freq = models.IntegerField(
        "Frequency of oscillations of alternating current  measured in hertz (Hz)",
            blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    pps = models.FloatField("Pulses per second", validators=[MinValueValidator(0)])
    pulse_dur = models.FloatField(
        "Pulse duration measured in pulses per second (PPS)",
            blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    duty_cycle = models.FloatField(
        "the fraction of one period in which a signal or system is active",
        blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    WAVEFORM_CHOICES = (
        ("SDC", "Smooth DC"),
        ("PDC", "Pulsed DC"),
        ("BPDC", "Burst of Pulses DC"),
        ("AC", "Alternating Current (AC)"),
        ("PAC", "Pulsed AC"),
        ("RDC", "Rectangular Wave DC"),
        ("RBDC", "Rectangular Wave Burst DC"),
    )
    waveform = models.CharField(
        help_text="",
        max_length=4,
        blank=True, null=True
        choices=WAVEFORM_CHOICES,
    )

    anodes = models.IntegerField(
        "Number of anode arrays.",
        blank=True, null=True,
        validators=[MinValueValidator(1)]
    )
    num_netters = models.IntegerField(
        "Number of people actively netting fish during sample or transect. ",
        blank=True, null=True,
        validators=[MinValueValidator(0)],
    )

    comment = models.TextField(blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ("effort",)

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}-electrofishing".format(self.effort.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())

        super(
            FN122ElectroFishing, self).save(*args, **kwargs)
