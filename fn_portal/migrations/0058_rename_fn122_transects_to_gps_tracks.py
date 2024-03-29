# Generated by Django 3.2.12 on 2022-11-16 17:10

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0057_lf_to_lifestage_rm_122_efftimes'),
    ]

    operations = [
        migrations.CreateModel(
            name='FN121GpsTrack',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('track_id', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('dd_lat', models.FloatField(validators=[django.core.validators.MinValueValidator(41.7), django.core.validators.MaxValueValidator(49.2)], verbose_name='Latitude (dd)')),
                ('dd_lon', models.FloatField(validators=[django.core.validators.MinValueValidator(-89.6), django.core.validators.MaxValueValidator(-76.4)], verbose_name='Longitude (dd)')),
                ('sidep', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(400)], verbose_name='Site Depth (m)')),
                ('comment', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(-81, 45), help_text='Represented as (longitude, latitude)', srid=4326, verbose_name='GPS Track Point')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gps_track_points', to='fn_portal.fn121')),
            ],
            options={
                'ordering': ('sample', 'track_id'),
                'unique_together': {('sample', 'track_id')},
            },
        ),
        migrations.DeleteModel(
            name='FN122Transect',
        ),
    ]
