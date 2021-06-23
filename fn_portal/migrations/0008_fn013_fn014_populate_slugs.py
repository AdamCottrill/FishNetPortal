# Generated by Django 2.2.23 on 2021-06-08 13:13

from django.db import migrations


class Migration(migrations.Migration):
    def fn013_slugs(apps, schema_editor):
        FN013 = apps.get_model("fn_portal", "FN013")
        for gear in FN013.objects.all():
            gear.slug = "-".join([gear.project.prj_cd, gear.gr])
            gear.save()

    def fn014_slugs(apps, schema_editor):
        FN014 = apps.get_model("fn_portal", "FN014")
        for panel in FN014.objects.all():
            panel.slug = "-".join([panel.gear.project.prj_cd, panel.gear.gr, panel.eff])
            panel.save()

    dependencies = [
        ("fn_portal", "0007_fn013_fn014_slugs_nullable"),
    ]

    operations = [migrations.RunPython(fn013_slugs), migrations.RunPython(fn014_slugs)]