# Generated by Django 2.2.23 on 2021-10-19 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0025_added_project_gear_process_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectgearprocesstype',
            unique_together={('project', 'gear', 'process_type')},
        ),
    ]