# Generated by Django 2.2.12 on 2020-05-20 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0006_auto_20200520_1421'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FN011',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(db_index=True, max_length=4)),
                ('prj_cd', models.CharField(db_index=True, max_length=13, unique=True)),
                ('slug', models.SlugField(max_length=13, unique=True)),
                ('prj_nm', models.CharField(max_length=255)),
                ('prj_date0', models.DateField()),
                ('prj_date1', models.DateField()),
                ('source', models.CharField(choices=[('offshore', 'Offshore Index'), ('nearshore', 'Nearshore Index'), ('smallfish', 'Smallfish Program')], default='offshore', max_length=255)),
                ('comment0', models.TextField(blank=True, null=True)),
                ('field_crew', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('lake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='common.Lake')),
                ('prj_ldr', models.ForeignKey(help_text='Project Lead', on_delete=django.db.models.deletion.CASCADE, related_name='creels', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-year', '-prj_date1'],
            },
        ),
        migrations.CreateModel(
            name='FN013',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gr', models.CharField(max_length=4)),
                ('effcnt', models.IntegerField(blank=True, null=True)),
                ('effdst', models.FloatField(blank=True, null=True)),
                ('gr_des', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gear', to='fn_portal.FN011')),
            ],
        ),
        migrations.CreateModel(
            name='FN121',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grtp', models.CharField(blank=True, db_index=True, max_length=3, null=True)),
                ('gr', models.CharField(blank=True, db_index=True, max_length=5, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sam', models.CharField(db_index=True, max_length=5)),
                ('effdt0', models.DateField(blank=True, db_index=True, null=True)),
                ('effdt1', models.DateField(blank=True, db_index=True, null=True)),
                ('effdur', models.FloatField(blank=True, null=True)),
                ('efftm0', models.TimeField(blank=True, db_index=True, null=True)),
                ('efftm1', models.TimeField(blank=True, db_index=True, null=True)),
                ('effst', models.CharField(blank=True, db_index=True, max_length=2, null=True)),
                ('orient', models.CharField(blank=True, db_index=True, max_length=2, null=True)),
                ('sidep', models.FloatField(blank=True, db_index=True, default=0, null=True)),
                ('secchi', models.FloatField(blank=True, null=True)),
                ('site', models.CharField(blank=True, max_length=100, null=True)),
                ('sitem', models.CharField(blank=True, max_length=5, null=True)),
                ('dd_lat', models.FloatField(blank=True, null=True)),
                ('dd_lon', models.FloatField(blank=True, null=True)),
                ('comment1', models.CharField(blank=True, max_length=500, null=True)),
                ('grid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fn_samples', to='common.Grid5')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='fn_portal.FN011')),
            ],
            options={
                'ordering': ['project', 'sam'],
                'unique_together': {('project', 'sam')},
            },
        ),
        migrations.CreateModel(
            name='FN122',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('eff', models.CharField(db_index=True, default=1, max_length=4)),
                ('effdst', models.FloatField(blank=True, null=True)),
                ('grdep', models.FloatField(blank=True, null=True)),
                ('grtem0', models.FloatField(blank=True, null=True)),
                ('grtem1', models.FloatField(blank=True, null=True)),
                ('waterhaul', models.BooleanField(default=False)),
                ('comment2', models.TextField(blank=True, null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effort', to='fn_portal.FN121')),
            ],
            options={
                'unique_together': {('sample', 'eff')},
            },
        ),
        migrations.CreateModel(
            name='FN123',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('grp', models.CharField(db_index=True, default='00', max_length=3)),
                ('catcnt', models.IntegerField(blank=True, null=True, verbose_name='Total Catch (numbers)')),
                ('count_only', models.IntegerField(blank=True, null=True, verbose_name='Fish counted but not sampled')),
                ('catwt', models.FloatField(blank=True, null=True, verbose_name='Total Catch Weight')),
                ('biocnt', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of fish bio-sampled')),
                ('comment', models.TextField(blank=True, null=True)),
                ('effort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catch', to='fn_portal.FN122')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catch_counts', to='common.Species')),
            ],
            options={
                'unique_together': {('effort', 'species', 'grp')},
            },
        ),
        migrations.CreateModel(
            name='FN125',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('fish', models.CharField(max_length=6)),
                ('flen', models.IntegerField(blank=True, null=True)),
                ('tlen', models.IntegerField(blank=True, null=True)),
                ('rwt', models.IntegerField(blank=True, null=True)),
                ('girth', models.IntegerField(blank=True, null=True)),
                ('clipa', models.CharField(blank=True, max_length=20, null=True)),
                ('clipc', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, db_index=True, max_length=2, null=True)),
                ('mat', models.CharField(blank=True, db_index=True, max_length=2, null=True)),
                ('gon', models.CharField(blank=True, db_index=True, max_length=4, null=True)),
                ('noda', models.CharField(blank=True, max_length=20, null=True)),
                ('nodc', models.CharField(blank=True, max_length=20, null=True)),
                ('agest', models.CharField(blank=True, max_length=20, null=True)),
                ('fate', models.CharField(blank=True, max_length=2, null=True)),
                ('age_flag', models.BooleanField(default=False)),
                ('stom_flag', models.BooleanField(default=False)),
                ('lam_flag', models.BooleanField(default=False)),
                ('tag_flag', models.BooleanField(default=False)),
                ('comment5', models.CharField(blank=True, max_length=500, null=True)),
                ('catch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fish', to='fn_portal.FN123')),
            ],
            options={
                'unique_together': {('catch', 'fish')},
            },
        ),
        migrations.CreateModel(
            name='FNProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True)),
                ('abbrev', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gr_label', models.CharField(max_length=100)),
                ('gr_code', models.CharField(db_index=True, max_length=4, unique=True)),
                ('effcnt', models.IntegerField(blank=True, null=True)),
                ('effdst', models.FloatField(blank=True, null=True)),
                ('gr_des', models.TextField(blank=True, null=True)),
                ('gr_des_html', models.TextField(blank=True, null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('depreciated', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gear2SubGear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panel_sequence', models.PositiveIntegerField(default=1)),
                ('panel_count', models.PositiveIntegerField(default=1)),
                ('gear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gang', to='fn_portal.Gear')),
            ],
            options={
                'ordering': ['panel_sequence', 'subgear__eff'],
            },
        ),
        migrations.CreateModel(
            name='GearFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=100)),
                ('abbrev', models.CharField(max_length=10, unique=True)),
                ('gear_type', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Gear Families',
            },
        ),
        migrations.CreateModel(
            name='SubGear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eff', models.CharField(blank=True, max_length=4, null=True)),
                ('mesh', models.FloatField(blank=True, null=True)),
                ('grlen', models.FloatField(blank=True, null=True)),
                ('grht', models.FloatField(blank=True, null=True)),
                ('grwid', models.FloatField(blank=True, null=True)),
                ('grcol', models.CharField(blank=True, choices=[('2', 'Black'), ('4', 'Blue'), ('7', 'Other'), ('8', 'Grey'), ('3', 'Green'), ('1', 'White'), ('6', 'Transparent'), ('5', 'Discoloured White')], max_length=10, null=True)),
                ('grmat', models.CharField(blank=True, choices=[('4', 'Polyester'), ('5', 'Cotton'), ('2', 'Polypropylene (e.g. Ulstron)'), ('6', 'Other'), ('3', 'Polyethylene'), ('1', 'Polyamide (e.g. Nylon)')], max_length=10, null=True)),
                ('gryarn', models.IntegerField(blank=True, choices=[(1, 'Monofilament'), (3, 'no data'), (2, 'Multifilament')], null=True)),
                ('grknot', models.IntegerField(blank=True, choices=[(3, 'other'), (2, 'Knots present'), (1, 'Knotless')], null=True)),
                ('grdiam', models.FloatField(blank=True, null=True)),
                ('tielength', models.FloatField(blank=True, null=True)),
                ('meshes_per_tie', models.PositiveIntegerField(blank=True, null=True)),
                ('meshes_deep', models.PositiveIntegerField(blank=True, null=True)),
                ('eff_des', models.TextField(blank=True, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subgears', to='fn_portal.GearFamily')),
                ('gear', models.ManyToManyField(related_name='subgears', through='fn_portal.Gear2SubGear', to='fn_portal.Gear')),
            ],
        ),
        migrations.AddField(
            model_name='gear2subgear',
            name='subgear',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gang', to='fn_portal.SubGear'),
        ),
        migrations.AddField(
            model_name='gear',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gears', to='fn_portal.GearFamily'),
        ),
        migrations.CreateModel(
            name='FN125_Lamprey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('lamid', models.IntegerField()),
                ('xlam', models.CharField(blank=True, max_length=6, null=True)),
                ('lamijc', models.CharField(blank=True, max_length=50, null=True)),
                ('lamijc_type', models.CharField(choices=[['0', '0'], ['a1', 'A1'], ['a2', 'A2'], ['a3', 'A3'], ['a4', 'A4'], ['b1', 'B1'], ['b2', 'B2'], ['b3', 'B3'], ['b4', 'B4']], default='0', max_length=2)),
                ('lamijc_size', models.IntegerField(blank=True, null=True)),
                ('comment_lam', models.TextField(blank=True, null=True)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lamprey_marks', to='fn_portal.FN125')),
            ],
            options={
                'ordering': ['slug', 'lamid'],
            },
        ),
        migrations.CreateModel(
            name='FN014',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eff', models.CharField(blank=True, max_length=4, null=True)),
                ('mesh', models.IntegerField(blank=True, null=True)),
                ('grlen', models.FloatField(blank=True, null=True)),
                ('grht', models.FloatField(blank=True, null=True)),
                ('grwid', models.FloatField(blank=True, null=True)),
                ('grcol', models.CharField(blank=True, max_length=10, null=True)),
                ('grmat', models.CharField(blank=True, max_length=10, null=True)),
                ('gryarn', models.IntegerField(blank=True, null=True)),
                ('grknot', models.IntegerField(blank=True, null=True)),
                ('eff_des', models.TextField(blank=True, null=True)),
                ('gear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gear_effs', to='fn_portal.FN013')),
            ],
            options={
                'ordering': ['eff'],
            },
        ),
        migrations.AddField(
            model_name='fn011',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='fn_portal.FNProtocol'),
        ),
        migrations.CreateModel(
            name='FN127',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('ageid', models.IntegerField()),
                ('agea', models.IntegerField(blank=True, db_index=True, null=True)),
                ('preferred', models.BooleanField(db_index=True, default=False)),
                ('agest', models.CharField(blank=True, db_index=True, max_length=5, null=True)),
                ('xagem', models.CharField(blank=True, max_length=2, null=True)),
                ('agemt', models.CharField(max_length=5)),
                ('edge', models.CharField(blank=True, max_length=2, null=True)),
                ('conf', models.IntegerField(blank=True, null=True)),
                ('nca', models.IntegerField(blank=True, null=True)),
                ('ageaDate', models.DateTimeField(blank=True, null=True)),
                ('comment7', models.TextField(blank=True, null=True)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='age_estimates', to='fn_portal.FN125')),
            ],
            options={
                'ordering': ['fish', 'ageid'],
                'unique_together': {('fish', 'ageid')},
            },
        ),
        migrations.CreateModel(
            name='FN126',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('food', models.IntegerField()),
                ('taxon', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('foodcnt', models.IntegerField(blank=True, null=True)),
                ('comment6', models.TextField(blank=True, null=True)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_data', to='fn_portal.FN125')),
            ],
            options={
                'ordering': ['fish', 'food'],
                'unique_together': {('fish', 'food')},
            },
        ),
        migrations.CreateModel(
            name='FN125Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('fish_tag_id', models.IntegerField()),
                ('tagstat', models.CharField(blank=True, db_index=True, max_length=5, null=True)),
                ('tagid', models.CharField(blank=True, max_length=9, null=True)),
                ('tagdoc', models.CharField(blank=True, db_index=True, max_length=6, null=True)),
                ('xcwtseq', models.CharField(blank=True, max_length=5, null=True)),
                ('xtaginckd', models.CharField(blank=True, max_length=6, null=True)),
                ('xtag_chk', models.CharField(blank=True, max_length=50, null=True)),
                ('comment_tag', models.TextField(blank=True, null=True)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fishtags', to='fn_portal.FN125')),
            ],
            options={
                'ordering': ['fish', 'fish_tag_id'],
                'unique_together': {('fish', 'fish_tag_id')},
            },
        ),
    ]