# Generated by Django 3.2.12 on 2022-04-22 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0037_add_FNPortalBaseModel_with_timestamps_FN011_status'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='fn012protocol',
            index=models.Index(fields=['lake', 'protocol'], name='fn_portal_f_lake_id_cdd166_idx'),
        ),
    ]
