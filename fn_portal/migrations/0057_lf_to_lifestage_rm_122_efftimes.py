# Generated by Django 3.2.12 on 2022-11-16 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0056_add_fn121_electrofishing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fn126',
            old_name='lf',
            new_name='lifestage',
        ),
        migrations.RemoveField(
            model_name='fn122',
            name='efftm0',
        ),
        migrations.RemoveField(
            model_name='fn122',
            name='efftm1',
        ),
    ]
