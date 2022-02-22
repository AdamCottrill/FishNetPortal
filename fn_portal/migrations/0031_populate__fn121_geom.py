# Generated by Django 2.2.23 on 2021-12-08 17:23

from django.db import migrations

# from django.db.models import F
# from django.contrib.gis.geos import Point


def populate_fn121_geom(apps, schema_editor):
    """Populate the geometry field for each record with the dd_lat and dd_lon"""

    FN121 = apps.get_model("fn_portal", "FN121")
    for x in FN121.objects.all():
        x.save()

    # (
    #     FN121.objects.exclude(dd_lat__isnull=True)
    #     .exclude(dd_lon__isnull=True)
    #     .bulk_update(geom=Point(F("dd_lon"), F("dd_lat")))
    # )


def clear_fn121_geom(apps, schema_editor):
    """"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("fn_portal", "0030_fn121_geom"),
    ]

    operations = [
        migrations.RunPython(populate_fn121_geom, reverse_code=clear_fn121_geom)
    ]