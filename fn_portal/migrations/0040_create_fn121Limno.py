# Generated by Django 3.2.12 on 2022-05-27 09:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fn_portal", "0039_update_fn012_constraints"),
    ]

    operations = [
        migrations.CreateModel(
            name="FN121Limno",
            fields=[
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                ("modified_timestamp", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                (
                    "sample",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="fn121_sample",
                        serialize=False,
                        to="fn_portal.fn121",
                    ),
                ),
                (
                    "do_gear",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ],
                        verbose_name="Dissolved Oxygen (mg/l) at Gear",
                    ),
                ),
                (
                    "xo2",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ],
                        verbose_name="Bottom Dissolved Oxygen (mg/l) [start]",
                    ),
                ),
                (
                    "xo22",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ],
                        verbose_name="Bottom Dissolved Oxygen (mg/l)  [end]",
                    ),
                ),
                (
                    "surfdo2",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ],
                        verbose_name="Surface Dissolved Oxygen (mg/l)  [start]",
                    ),
                ),
                (
                    "surfdo22",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ],
                        verbose_name="Surface Dissolved Oxygen (mg/l) [end]",
                    ),
                ),
            ],
            options={
                "ordering": ["slug"],
            },
        ),
    ]
