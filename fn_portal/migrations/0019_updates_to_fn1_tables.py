# Generated by Django 2.2.23 on 2021-08-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0018_remove_gr_grtp_from_fn121'),
    ]

    operations = [
        migrations.AddField(
            model_name='fn123',
            name='subcnt',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of Fish in Subsample'),
        ),
        migrations.AddField(
            model_name='fn123',
            name='subwt',
            field=models.FloatField(blank=True, null=True, verbose_name='Subsample Weight (kg)'),
        ),
        migrations.AddField(
            model_name='fn125',
            name='tissue',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='fn126',
            name='fdmes',
            field=models.CharField(blank=True, choices=[(None, 'No Data'), ('L', 'Length'), ('W', 'Weight'), ('V', 'Volume')], help_text='Food Measure Code', max_length=2),
        ),
        migrations.AddField(
            model_name='fn126',
            name='foodval',
            field=models.FloatField(blank=True, null=True, verbose_name='Food Measure Value'),
        ),
        migrations.AddField(
            model_name='fn126',
            name='lf',
            field=models.CharField(blank=True, choices=[(None, 'No Data'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('60', '60')], help_text='Life Stage', max_length=2),
        ),
        migrations.AlterField(
            model_name='fn123',
            name='catwt',
            field=models.FloatField(blank=True, null=True, verbose_name='Total Catch Weight (kg)'),
        ),
        migrations.AlterField(
            model_name='fn125tag',
            name='fish_tag_id',
            field=models.IntegerField(verbose_name='Identifier for a Fn125_tag record'),
        ),
        migrations.AlterField(
            model_name='fn125tag',
            name='tagdoc',
            field=models.CharField(blank=True, db_index=True, max_length=6, null=True, verbose_name='Tag Documentation'),
        ),
        migrations.AlterField(
            model_name='fn125tag',
            name='tagid',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='Tag Identification'),
        ),
        migrations.AlterField(
            model_name='fn125tag',
            name='tagstat',
            field=models.CharField(blank=True, db_index=True, max_length=5, null=True, verbose_name='Tag Status'),
        ),
        migrations.AlterField(
            model_name='fn125tag',
            name='xcwtseq',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Sequential CWT number'),
        ),
        migrations.AlterField(
            model_name='fn126',
            name='food',
            field=models.IntegerField(verbose_name='Food Id'),
        ),
        migrations.AlterField(
            model_name='fn126',
            name='foodcnt',
            field=models.IntegerField(blank=True, null=True, verbose_name='Food Count'),
        ),
        migrations.AlterField(
            model_name='fn126',
            name='taxon',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='A taxonomic code used to identify the type of food item.'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='agea',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Age Assessed (yr)'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='ageid',
            field=models.IntegerField(verbose_name='An identifier for an age estimate record'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='agemt',
            field=models.CharField(max_length=5, verbose_name='Age Method Data'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='agest',
            field=models.CharField(blank=True, db_index=True, max_length=5, null=True, verbose_name='Age Structure'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='conf',
            field=models.IntegerField(blank=True, null=True, verbose_name='Confidence'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='edge',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Edge Code'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='nca',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of Complete Annuli'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='preferred',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Preferred age estimate for a fish'),
        ),
        migrations.AlterField(
            model_name='fn127',
            name='xagem',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Age Assigned Method'),
        ),
    ]
