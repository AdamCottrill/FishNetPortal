# Generated by Django 3.2.12 on 2022-10-06 11:55

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_add_vessel_lookup'),
        ('fn_portal', '0046_rename_limno_fields_and_xfields'),
    ]

    operations = [
        migrations.CreateModel(
            name='FN121Weather',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='weather_data', serialize=False, to='fn_portal.fn121')),
                ('airtem0', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(45)], verbose_name='Air temperature (C) at the sampling site at the time when sampling starts')),
                ('airtem1', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(45)], verbose_name='Air temperature (C) at the sampling site at the time when sampling ends')),
                ('wind_speed0', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Wind wind speed in knots at the time when sampling starts.')),
                ('wind_speed1', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Wind wind speed in knots at the time when sampling ends.')),
                ('wind_direction0', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(360)], verbose_name='Wind wind direction in degrees at the time when sampling starts.')),
                ('wind_direction1', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(360)], verbose_name='Wind wind direction in degrees at the time when sampling ends.')),
                ('precip0', models.CharField(blank=True, choices=[('00', 'none'), ('10', 'mist'), ('40', 'fog'), ('51', 'slight drizzle'), ('55', 'heavy drizzle'), ('61', 'light rain'), ('65', 'heavy rain'), ('71', 'light snow'), ('75', 'heavy snow'), ('80', 'light rain shower'), ('85', 'heavy rain shower'), ('95', 'thunder storm')], max_length=2, null=True, verbose_name='The type of precipitation, fog or mist the time when sampling starts.')),
                ('precip1', models.CharField(blank=True, choices=[('00', 'none'), ('10', 'mist'), ('40', 'fog'), ('51', 'slight drizzle'), ('55', 'heavy drizzle'), ('61', 'light rain'), ('65', 'heavy rain'), ('71', 'light snow'), ('75', 'heavy snow'), ('80', 'light rain shower'), ('85', 'heavy rain shower'), ('95', 'thunder storm')], max_length=2, null=True, verbose_name='The type of precipitation, fog or mist the time when sampling ends.')),
                ('cloud_pc0', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(100)], verbose_name='Cloud cover, expressed as a percent at the time when sampling starts.')),
                ('cloud_pc1', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(100)], verbose_name='Cloud cover, expressed as a percent at the time when sampling ends.')),
                ('waveht0', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(10)], verbose_name='Wave height measured in meters (m) at the time when sampling starts.')),
                ('waveht1', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(10)], verbose_name='Wave height measured in meters (m) at the time when sampling ends.')),
                ('precip_duration', models.IntegerField(blank=True, choices=[(1, 'no precipitation'), (2, '< 4 hours of precipitation'), (3, '> 4 hours of precipitation'), (4, 'constant precipitation')], null=True, verbose_name='duration of precipitation for the set')),
                ('wave_duration', models.IntegerField(blank=True, choices=[(1, 'no precipitation'), (2, '< 4 hours of precipitation'), (3, '> 4 hours of precipitation'), (4, 'constant precipitation')], null=True, verbose_name='duration of waves for the set')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.AlterField(
            model_name='fn121limno',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='limno_data', serialize=False, to='fn_portal.fn121'),
        ),
        migrations.CreateModel(
            name='FN121Trawl',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='trawl_data', serialize=False, to='fn_portal.fn121')),
                ('vessel_speed', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='The speed of the research vessel (knots) during the sample.')),
                ('vessel_direction', models.IntegerField(blank=True, choices=[(0, 'Variable'), (1, 'Northeast'), (2, 'East'), (3, 'Southeast'), (4, 'South'), (5, 'Southwest'), (6, 'West'), (7, 'Northwest'), (8, 'North'), (9, 'Not Definable')], null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='The direction the vessel was traveling during the sample')),
                ('warp', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Trawl Gear Warp (tow line) Length expressed in meters (m).')),
                ('vessel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trawl_samples', to='common.vessel')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='FN121Trapnet',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='trapnet_data', serialize=False, to='fn_portal.fn121')),
                ('vegetation', models.IntegerField(blank=True, choices=[(1, 'None'), (2, 'Sparse (1-25%)'), (3, 'Moderate (25-75%)'), (4, 'Dense (>75%)')], null=True, verbose_name='Observed aquatic vegetation density.')),
                ('lead_angle', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(90)], verbose_name='The angle that gear was set relative to the shoreline')),
                ('leaduse', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Length of leader in the water (m)')),
                ('distoff', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='The distance between the shore and the start of the lead')),
                ('bottom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='common.bottomtype')),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='common.covertype')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='FN123NonFish',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('catcnt', models.IntegerField(blank=True, null=True, verbose_name='Total Catch (numbers, including both dead and alive)')),
                ('mortcnt', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of dead individuals.')),
                ('comment3', models.TextField(blank=True, null=True)),
                ('effort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='non_fish_catch', to='fn_portal.fn122')),
                ('taxon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fn_catch_counts', to='common.taxon')),
            ],
            options={
                'ordering': ('effort', 'taxon'),
                'unique_together': {('effort', 'taxon')},
            },
        ),
        migrations.CreateModel(
            name='FN122Transect',
            fields=[
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('track_id', models.IntegerField()),
                ('dd_lat', models.FloatField(verbose_name='Latitude (dd)')),
                ('dd_lon', models.FloatField(verbose_name='Longitude (dd)')),
                ('sidep', models.FloatField(blank=True, null=True, verbose_name='Site Depth (m)')),
                ('comment', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(-81, 45), help_text='Represented as (longitude, latitude)', srid=4326, verbose_name='Transect Point')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transect_points', to='fn_portal.fn121')),
            ],
            options={
                'ordering': ('sample', 'track_id'),
                'unique_together': {('sample', 'track_id')},
            },
        ),
    ]
