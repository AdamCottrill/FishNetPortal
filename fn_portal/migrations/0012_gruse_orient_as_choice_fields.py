# Generated by Django 2.2.23 on 2021-08-10 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fn_portal", "0011_update_fn121_fks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fn028",
            name="gruse",
            field=models.CharField(
                choices=[
                    ("1", "Bottom"),
                    ("2", "Canned"),
                    ("3", "Kyted"),
                    ("9", "Unknown"),
                ],
                default="1",
                help_text="Code to identify how a gear was used",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="fn028",
            name="orient",
            field=models.CharField(
                choices=[
                    ("1", "Perpendicular"),
                    ("2", "Paralell"),
                    ("9", "Unknown"),
                    ("U", "Upstream"),
                    ("D", "Downstream"),
                ],
                default="9",
                help_text="Gear Orientation",
                max_length=2,
            ),
        ),
    ]
