# Generated by Django 2.2.23 on 2021-10-19 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0023_populate_gear_process_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fn026',
            old_name='ddlat',
            new_name='dd_lat',
        ),
        migrations.RenameField(
            model_name='fn026',
            old_name='ddlon',
            new_name='dd_lon',
        ),
    ]
