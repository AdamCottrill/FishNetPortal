# Generated by Django 3.2.12 on 2022-08-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0042_unique_fn127_fish_preferred_true'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='fn127',
            index=models.Index(fields=['fish', 'ageid', 'preferred'], name='fn_portal_f_fish_id_f0e0ba_idx'),
        ),
    ]
