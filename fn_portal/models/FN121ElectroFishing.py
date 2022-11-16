from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121


class FN121ElectroFishing(FNPortalBaseModel):
    """A table to hold information about electrofishing settings and
    effort - volts, amps, waveform, total seconds. ect. Associated
    with a specific elecro fishing FN121 record. Modeled as an
    optional 1:1 record.

    """

    sample = models.OneToOneField(
        FN121,
        related_name="electro_fishing_data",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    shock_sec = models.IntegerField(
        "A measure of shocking effort, measured in seconds.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
    )

    volts_min = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
    )

    volts_max = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
    )
    volts_mean = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1200)],
    )

    amps_min = models.FloatField(
        "Minimum current observed a sample or transect.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(80)],
    )
    amps_max = models.FloatField(
        "Maximum current observed a sample or transect.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(80)],
    )
    amps_mean = models.FloatField(
        "Mean current observed a sample or transect.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(80)],
    )

    power_min = models.FloatField(
        "Minimum power output during an electrofishing sample.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(15000)],
    )

    power_max = models.FloatField(
        "Maximum power output during an electrofishing sample.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(15000)],
    )

    power_mean = models.FloatField(
        "Maximum power output during an electrofishing sample.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(15000)],
    )

    conduct = models.FloatField(
        "Measured conductivity of the water in microsiemens (microS).",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )

    turbidity = models.FloatField(
        "Measured turbidity of the water within a sample, measured in NTU:",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(400)],
    )

    freq = models.IntegerField(
        "Frequency of oscillations of alternating current  measured in hertz (Hz)",
        blank=True,
        null=True,
        validators=[MinValueValidator(10), MaxValueValidator(250)],
    )

    pulse_dur = models.FloatField(
        "Pulse duration measured in pulses per second (PPS)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )

    pulse_pattern = models.CharField(
        help_text="Pulse pattern...",
        max_length=100,
        blank=True,
        null=True,
    )

    duty_cycle = models.FloatField(
        "The fraction of one period in which a signal or system is active",
        blank=True,
        null=True,
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
        help_text="The type of electrical waveform created by the electrofishing unit.",
        max_length=4,
        blank=True,
        null=True,
        choices=WAVEFORM_CHOICES,
    )

    anodes = models.IntegerField(
        "Number of anode arrays.",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
    )
    num_netters = models.IntegerField(
        "Number of people actively netting fish during sample or transect. ",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(8)],
    )

    comment = models.TextField(blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ("sample",)

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-electrofishing".format(self.sample.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        self.full_clean()

        super(FN121ElectroFishing, self).save(*args, **kwargs)
