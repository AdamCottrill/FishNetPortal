# Generated by Django 3.2.12 on 2022-10-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0051_fn121trawls_optional_vessel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fn125',
            name='stom_flag',
            field=models.CharField(choices=[('0', 'Not Collected'), ('1', 'FN126 Records'), ('2', 'External Database')], default=0, help_text='Was a stomach sample collected?', max_length=1),
        ),
    ]
