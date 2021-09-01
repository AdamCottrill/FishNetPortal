# Generated by Django 2.2.23 on 2021-05-26 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fn_portal", "0004_auto_20200606_0911"),
    ]

    operations = [
        migrations.CreateModel(
            name="FN028",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        db_index=True, help_text="Mode Code", max_length=2
                    ),
                ),
                (
                    "mode_des",
                    models.CharField(
                        help_text="Fishing Mode Description", max_length=100
                    ),
                ),
                (
                    "gr",
                    models.CharField(
                        help_text="Fishing Mode Description", max_length=4
                    ),
                ),
                (
                    "gruse",
                    models.CharField(
                        help_text="Code to identify how a gear was used", max_length=2
                    ),
                ),
                (
                    "orient",
                    models.CharField(help_text="Gear Orientation", max_length=2),
                ),
                (
                    "effdur_ge",
                    models.IntegerField(
                        blank=True,
                        help_text="The minimum duration of a fishing effort.",
                        null=True,
                    ),
                ),
                (
                    "effdur_lt",
                    models.IntegerField(
                        blank=True,
                        help_text="The maximum duration of a fishing effort.",
                        null=True,
                    ),
                ),
                (
                    "efftm0_ge",
                    models.TimeField(
                        blank=True,
                        help_text="The earliest time of day that fishing effort starts",
                        null=True,
                    ),
                ),
                (
                    "efftm0_lt",
                    models.TimeField(
                        blank=True,
                        help_text="The latest time of day that fishing effort starts",
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(blank=True, editable=False, unique=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modes",
                        to="fn_portal.FN011",
                    ),
                ),
            ],
            options={
                "verbose_name": "FN028 - Fishing Mode",
                "ordering": ["mode"],
                "unique_together": {("project", "mode")},
            },
        ),
        migrations.CreateModel(
            name="FN026",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(help_text="Space Label", max_length=110)),
                (
                    "space",
                    models.CharField(
                        db_index=True, help_text="Space Code", max_length=2
                    ),
                ),
                (
                    "space_des",
                    models.CharField(help_text="Space Description", max_length=100),
                ),
                (
                    "space_siz",
                    models.IntegerField(
                        blank=True,
                        help_text="The relative size of a space (i.e. spatial stratum).",
                        null=True,
                    ),
                ),
                (
                    "area_lst",
                    models.CharField(help_text="Space Description", max_length=100),
                ),
                (
                    "aru",
                    models.CharField(
                        help_text="Aquatic Resource Unit Id", max_length=100
                    ),
                ),
                (
                    "grdep_ge",
                    models.FloatField(
                        blank=True,
                        help_text="The lower limit of gear depth (in metres).",
                        null=True,
                    ),
                ),
                (
                    "grdep_lt",
                    models.FloatField(
                        blank=True,
                        help_text="The upper limit of gear depth (in metres).",
                        null=True,
                    ),
                ),
                (
                    "sidep_ge",
                    models.FloatField(
                        blank=True,
                        help_text="The upper depth limit (in metres) of sites that belong to the corresponding spatial stratum",
                        null=True,
                    ),
                ),
                (
                    "sidep_lt",
                    models.FloatField(
                        blank=True,
                        help_text="The lower depth limit (in metres) of sites that belong to the corresponding spatial stratum. ",
                        null=True,
                    ),
                ),
                (
                    "grid_ge",
                    models.IntegerField(
                        blank=True,
                        help_text="The lower limit of grid values belonging to a spatial stratum",
                        null=True,
                    ),
                ),
                (
                    "grid_lt",
                    models.IntegerField(
                        blank=True,
                        help_text="The upper limit of grid values belonging to a spatial stratum",
                        null=True,
                    ),
                ),
                (
                    "site_lst",
                    models.CharField(
                        blank=True,
                        help_text="A list of SITEs that belong to the corresponding spatial stratum",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "sitp_lst",
                    models.CharField(
                        blank=True,
                        help_text="A list of site types, delimited by comma",
                        max_length=100,
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(blank=True, editable=False, unique=True)),
                ("ddlat", models.FloatField(blank=True, null=True)),
                ("ddlon", models.FloatField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="spatial_strata",
                        to="fn_portal.FN011",
                    ),
                ),
            ],
            options={
                "verbose_name": "FN026 - Spatial Strata",
                "verbose_name_plural": "FN026 - Spatial Strata",
                "ordering": ["space"],
                "unique_together": {("project", "space")},
            },
        ),
        migrations.CreateModel(
            name="FN022",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ssn",
                    models.CharField(
                        db_index=True, help_text="Season Code", max_length=2
                    ),
                ),
                (
                    "ssn_des",
                    models.CharField(help_text="Season Description", max_length=60),
                ),
                ("ssn_date0", models.DateField(help_text="Season Start Date")),
                ("ssn_date1", models.DateField(help_text="Season End Date")),
                ("v0", models.CharField(max_length=4)),
                ("slug", models.SlugField(blank=True, editable=False, unique=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seasons",
                        to="fn_portal.FN011",
                    ),
                ),
            ],
            options={
                "verbose_name": "FN022 - Season",
                "ordering": ["ssn"],
                "unique_together": {("project", "ssn")},
            },
        ),
    ]
