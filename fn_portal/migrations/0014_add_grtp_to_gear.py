# Generated by Django 2.2.23 on 2021-08-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0013_fn022_ssndate0_ssndate1_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='gear',
            name='grtp',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Gear Type'),
        ),
        migrations.AlterField(
            model_name='gear',
            name='effcnt',
            field=models.IntegerField(blank=True, null=True, verbose_name='Effort Count'),
        ),
        migrations.AlterField(
            model_name='gear',
            name='effdst',
            field=models.FloatField(blank=True, null=True, verbose_name='Effort Distance(m)'),
        ),
        migrations.AlterField(
            model_name='gear',
            name='gr_code',
            field=models.CharField(db_index=True, max_length=4, unique=True, verbose_name='Gear Code'),
        ),
        migrations.AlterField(
            model_name='gear',
            name='gr_des',
            field=models.TextField(blank=True, null=True, verbose_name='Gear Description'),
        ),
        migrations.AlterField(
            model_name='gear',
            name='gr_label',
            field=models.CharField(max_length=100, verbose_name='Gear Label'),
        ),
    ]
