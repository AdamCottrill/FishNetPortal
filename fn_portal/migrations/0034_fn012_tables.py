# Generated by Django 2.2.23 on 2022-03-04 08:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("fn_portal", "0034_fn012_and_fn012Defaults_tables"),
        ("fn_portal", "0035_fn012_allow_null_fdsam2_and_agedec2"),
        ("fn_portal", "0036_rename_fn012Default_to_FN012Protocol"),
        ("fn_portal", "0037_remove_flen2tlen_from_fn012_tables"),
        ("fn_portal", "0038_add_fn012_lammrk"),
        ("fn_portal", "0039_populate_fn012Protocol"),
    ]

    dependencies = [
        ("fn_portal", "0033_FN126_update_food_to_fd"),
        ("common", "0007_species_fn012_fields"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fn011",
            options={
                "ordering": ["-year", "prj_cd"],
                "verbose_name_plural": "FN011 - Projects",
            },
        ),
        migrations.CreateModel(
            name="FN012",
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
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("grp", models.CharField(db_index=True, default="00", max_length=3)),
                (
                    "grp_des",
                    models.CharField(
                        default="Default Group",
                        help_text="The meaning of a GRP code or more general information about SPC+GRP.",
                        max_length=300,
                    ),
                ),
                (
                    "biosam",
                    models.CharField(
                        choices=[
                            ("0", "Not sampled"),
                            ("1", "Complete sampling"),
                            ("2", "Random sampling"),
                            ("3", "Size-stratified sampling"),
                        ],
                        default="1",
                        help_text="Biosampling Code",
                        max_length=1,
                    ),
                ),
                (
                    "sizsam",
                    models.CharField(
                        choices=[
                            ("0", "Not Sampled"),
                            ("1", "FN125"),
                            ("2", "FN124"),
                            ("3", "Both FN124 and FN125"),
                        ],
                        default=0,
                        help_text="Size Sample Code",
                        max_length=1,
                    ),
                ),
                (
                    "sizatt",
                    models.CharField(
                        blank=True,
                        choices=[("FLEN", "Fork Length"), ("TLEN", "Total Length")],
                        default="FLEN",
                        help_text="Size Sample Code",
                        max_length=4,
                        null=True,
                    ),
                ),
                (
                    "sizint",
                    models.IntegerField(
                        default=1,
                        help_text="Size Sample Interval (mm)",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(50),
                        ],
                    ),
                ),
                (
                    "fdsam1",
                    models.CharField(
                        choices=[
                            ("0", "Data not collected"),
                            ("1", "Collected, not processed"),
                            ("2", "Collected, processed"),
                        ],
                        default="0",
                        help_text="FDSAM Sampling Status",
                        max_length=1,
                    ),
                ),
                (
                    "fdsam2",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "1",
                                "Fish Community and Habitat Section (FCH), Fisheries Branch",
                            ),
                            ("2", "Haliburton Hastings Fisheries Assessment Unit"),
                            ("3", "Other"),
                        ],
                        help_text="FDSAM Taxon Coding Scheme",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "spcmrk1",
                    models.CharField(
                        choices=[
                            ("0", "No marks exist & none applied"),
                            ("1", "Marks exist & none applied"),
                            ("2", "No marks exist & marks applied"),
                            ("3", "Marks exist & marks applied"),
                        ],
                        default="0",
                        help_text="Species Mark Exists",
                        max_length=1,
                    ),
                ),
                (
                    "spcmrk2",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("0", "Marks not unique marks"),
                            ("1", "Marks unique"),
                            ("2", "Marks unique and non-unique"),
                        ],
                        help_text="Species Mark Unique",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "agedec1",
                    models.CharField(
                        choices=[
                            ("0", "No structures sampled"),
                            ("1", "Scales (any side)"),
                            ("2", "Scales (left side)"),
                            ("3", "Scales (right side)"),
                            ("4", "Pectoral ray"),
                            ("5", "Pectoral spine"),
                            ("6", "Pelvic ray"),
                            ("7", "Dorsal spine"),
                            ("A", "Otolith"),
                            ("B", "Operculum"),
                            ("C", "Sub-operculum"),
                            ("D", "Cleithrum"),
                            ("E", "Centrum"),
                            ("F", "Branchiostegal"),
                            ("G", "Other (NO LONGER SUPPORTED)"),
                            ("M", "Maxilla"),
                            ("T", "Tag"),
                            ("V", "Vertebrate"),
                            ("X", "Methods vary across fish"),
                        ],
                        default="0",
                        help_text="Age Method",
                        max_length=1,
                    ),
                ),
                (
                    "agedec2",
                    models.CharField(
                        blank=True,
                        choices=[("0", "Not validated"), ("1", "Validated")],
                        help_text="Age Method",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "flen_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(700),
                        ],
                        verbose_name="Minimum Fork Length (mm)",
                    ),
                ),
                (
                    "flen_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(2000),
                        ],
                        verbose_name="Maximim Fork Length (mm)",
                    ),
                ),
                (
                    "tlen_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(700),
                        ],
                        verbose_name="Minimum Total Length (mm)",
                    ),
                ),
                (
                    "tlen_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(2000),
                        ],
                        verbose_name="Maximum Total Length (mm)",
                    ),
                ),
                (
                    "rwt_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5000),
                        ],
                        verbose_name="Minimum Round Weight (g)",
                    ),
                ),
                (
                    "rwt_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5000),
                        ],
                        verbose_name="Maximum Round Weight (g)",
                    ),
                ),
                (
                    "k_min_error",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(2.0),
                        ],
                        verbose_name="Minimum K (TLEN) - error",
                    ),
                ),
                (
                    "k_min_warn",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1.5),
                        ],
                        verbose_name="Minimum K (TLEN) - warning",
                    ),
                ),
                (
                    "k_max_error",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5.0),
                        ],
                        verbose_name="Maximum K (FLEN) - error",
                    ),
                ),
                (
                    "k_max_warn",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4.0),
                        ],
                        verbose_name="Maximum K (FLEN) - warning",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sample_specs",
                        to="fn_portal.FN011",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fn012_sample_specs",
                        to="common.Species",
                    ),
                ),
                (
                    "lamsam",
                    models.CharField(
                        choices=[
                            ("0", "Not Collected"),
                            ("1", "XLAM (NO LONGER SUPPORTED)"),
                            ("2", "LAMIJC"),
                        ],
                        default=2,
                        help_text="Lamprey Reporting",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "FN012 - Project Sampling Specs",
            },
        ),
        migrations.CreateModel(
            name="FN012Protocol",
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
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("grp", models.CharField(db_index=True, default="00", max_length=3)),
                (
                    "grp_des",
                    models.CharField(
                        default="Default Group",
                        help_text="The meaning of a GRP code or more general information about SPC+GRP.",
                        max_length=300,
                    ),
                ),
                (
                    "biosam",
                    models.CharField(
                        choices=[
                            ("0", "Not sampled"),
                            ("1", "Complete sampling"),
                            ("2", "Random sampling"),
                            ("3", "Size-stratified sampling"),
                        ],
                        default="1",
                        help_text="Biosampling Code",
                        max_length=1,
                    ),
                ),
                (
                    "sizsam",
                    models.CharField(
                        choices=[
                            ("0", "Not Sampled"),
                            ("1", "FN125"),
                            ("2", "FN124"),
                            ("3", "Both FN124 and FN125"),
                        ],
                        default=0,
                        help_text="Size Sample Code",
                        max_length=1,
                    ),
                ),
                (
                    "sizatt",
                    models.CharField(
                        blank=True,
                        choices=[("FLEN", "Fork Length"), ("TLEN", "Total Length")],
                        default="FLEN",
                        help_text="Size Sample Code",
                        max_length=4,
                        null=True,
                    ),
                ),
                (
                    "sizint",
                    models.IntegerField(
                        default=1,
                        help_text="Size Sample Interval (mm)",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(50),
                        ],
                    ),
                ),
                (
                    "fdsam1",
                    models.CharField(
                        choices=[
                            ("0", "Data not collected"),
                            ("1", "Collected, not processed"),
                            ("2", "Collected, processed"),
                        ],
                        default="0",
                        help_text="FDSAM Sampling Status",
                        max_length=1,
                    ),
                ),
                (
                    "fdsam2",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "1",
                                "Fish Community and Habitat Section (FCH), Fisheries Branch",
                            ),
                            ("2", "Haliburton Hastings Fisheries Assessment Unit"),
                            ("3", "Other"),
                        ],
                        help_text="FDSAM Taxon Coding Scheme",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "spcmrk1",
                    models.CharField(
                        choices=[
                            ("0", "No marks exist & none applied"),
                            ("1", "Marks exist & none applied"),
                            ("2", "No marks exist & marks applied"),
                            ("3", "Marks exist & marks applied"),
                        ],
                        default="0",
                        help_text="Species Mark Exists",
                        max_length=1,
                    ),
                ),
                (
                    "spcmrk2",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("0", "Marks not unique marks"),
                            ("1", "Marks unique"),
                            ("2", "Marks unique and non-unique"),
                        ],
                        help_text="Species Mark Unique",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "agedec1",
                    models.CharField(
                        choices=[
                            ("0", "No structures sampled"),
                            ("1", "Scales (any side)"),
                            ("2", "Scales (left side)"),
                            ("3", "Scales (right side)"),
                            ("4", "Pectoral ray"),
                            ("5", "Pectoral spine"),
                            ("6", "Pelvic ray"),
                            ("7", "Dorsal spine"),
                            ("A", "Otolith"),
                            ("B", "Operculum"),
                            ("C", "Sub-operculum"),
                            ("D", "Cleithrum"),
                            ("E", "Centrum"),
                            ("F", "Branchiostegal"),
                            ("G", "Other (NO LONGER SUPPORTED)"),
                            ("M", "Maxilla"),
                            ("T", "Tag"),
                            ("V", "Vertebrate"),
                            ("X", "Methods vary across fish"),
                        ],
                        default="0",
                        help_text="Age Method",
                        max_length=1,
                    ),
                ),
                (
                    "agedec2",
                    models.CharField(
                        blank=True,
                        choices=[("0", "Not validated"), ("1", "Validated")],
                        help_text="Age Method",
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "flen_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(700),
                        ],
                        verbose_name="Minimum Fork Length (mm)",
                    ),
                ),
                (
                    "flen_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(2000),
                        ],
                        verbose_name="Maximim Fork Length (mm)",
                    ),
                ),
                (
                    "tlen_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(700),
                        ],
                        verbose_name="Minimum Total Length (mm)",
                    ),
                ),
                (
                    "tlen_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(2000),
                        ],
                        verbose_name="Maximum Total Length (mm)",
                    ),
                ),
                (
                    "rwt_min",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5000),
                        ],
                        verbose_name="Minimum Round Weight (g)",
                    ),
                ),
                (
                    "rwt_max",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5000),
                        ],
                        verbose_name="Maximum Round Weight (g)",
                    ),
                ),
                (
                    "k_min_error",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(2.0),
                        ],
                        verbose_name="Minimum K (TLEN) - error",
                    ),
                ),
                (
                    "k_min_warn",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1.5),
                        ],
                        verbose_name="Minimum K (TLEN) - warning",
                    ),
                ),
                (
                    "k_max_error",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5.0),
                        ],
                        verbose_name="Maximum K (FLEN) - error",
                    ),
                ),
                (
                    "k_max_warn",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4.0),
                        ],
                        verbose_name="Maximum K (FLEN) - warning",
                    ),
                ),
                (
                    "lake",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sample_specs",
                        to="common.Lake",
                    ),
                ),
                (
                    "protocol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sample_specs",
                        to="fn_portal.FNProtocol",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fn012protocol_sample_specs",
                        to="common.Species",
                    ),
                ),
                (
                    "lamsam",
                    models.CharField(
                        choices=[
                            ("0", "Not Collected"),
                            ("1", "XLAM (NO LONGER SUPPORTED)"),
                            ("2", "LAMIJC"),
                        ],
                        default=2,
                        help_text="Lamprey Reporting",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "FN012Protocols - Protocol Sampling Specs",
            },
        ),
        migrations.RunSQL(
            sql="\n          -- initial values of FN012Protocol table\n            INSERT INTO fn_portal_fn012protocol\n            (\n              slug,\n              lake_id,\n              protocol_id,\n              species_id,\n              grp,\n              grp_des,\n              biosam,\n              sizsam,\n              sizatt,\n              sizint,\n              agedec1,\n              fdsam1,\n              spcmrk1,\n              lamsam,\n              flen_min,\n              flen_max,\n              tlen_min,\n              tlen_max,\n              rwt_min,\n              rwt_max,\n              k_min_error,\n              k_min_warn,\n              k_max_error,\n              k_max_warn\n            )\n            SELECT DISTINCT\n            lower('fn012protocol-' || common_lake.abbrev || '-' ||fnprotocol.abbrev || '-' || spc.spc || '-' || grp) as slug,\n            common_lake.id AS lake_id,\n                   fnprotocol.id AS protocol_id,\n                   spc.id AS species_id,\n                   grp,\n                   'default group' AS grp_des,\n                   '0' AS biosam,\n                   '0' AS sizsam,\n                   'flen' AS sizatt,\n                   1 AS sizint,\n                   '0' AS agedec1,\n                   '0' AS fdsam1,\n                   '0' AS spcmrk1,\n                   '2' as lamsam,\n                   flen_min,\n                   flen_max,\n                   tlen_min,\n                   tlen_max,\n                   rwt_min,\n                   rwt_max,\n                   k_min_error,\n                   k_min_warn,\n                   k_max_error,\n                   k_max_warn\n            FROM fn_portal_fn123 AS fn123\n              JOIN common_species AS spc ON spc.id = fn123.species_id\n              JOIN fn_portal_fn122 AS fn122 ON fn122.id = fn123.effort_id\n              JOIN fn_portal_fn121 AS fn121 ON fn121.id = fn122.sample_id\n              JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id\n              JOIN common_lake ON common_lake.id = fn011.lake_id\n              JOIN fn_portal_fnprotocol AS fnprotocol ON fnprotocol.id = fn011.protocol_id\n            WHERE spc.spc NOT IN ('000','999','998')\n            ORDER BY common_lake.id,\n                     fnprotocol.id,\n                     spc.id,\n                     grp;\n                        ",
            reverse_sql="DELETE FROM fn_portal_fn012protocol;",
        ),
    ]
