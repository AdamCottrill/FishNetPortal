# Generated by Django 2.2.12 on 2020-06-06 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fn_portal", "0002_longer_tagid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fn011",
            name="field_crew",
            field=models.ManyToManyField(
                related_name="fn_field_crew", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="fn011",
            name="prj_ldr",
            field=models.ForeignKey(
                help_text="Project Lead",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fn_projects",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="fn123",
            name="species",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="common.Species"
            ),
        ),
    ]
