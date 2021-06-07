# Generated by Django 2.2.23 on 2021-06-07 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fn_portal', '0005_FN022_FN026_FN028_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subgear',
            name='grcol',
            field=models.CharField(blank=True, choices=[('1', 'White'), ('2', 'Black'), ('3', 'Green'), ('4', 'Blue'), ('5', 'Discoloured White'), ('6', 'Transparent'), ('7', 'Other'), ('8', 'Grey')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='subgear',
            name='grmat',
            field=models.CharField(blank=True, choices=[('1', 'Polyamide (e.g. Nylon)'), ('2', 'Polypropylene (e.g. Ulstron)'), ('3', 'Polyethylene'), ('4', 'Polyester'), ('5', 'Cotton'), ('6', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='subgear',
            name='gryarn',
            field=models.IntegerField(blank=True, choices=[(1, 'Monofilament'), (2, 'Multifilament'), (3, 'no data')], null=True),
        ),
        migrations.CreateModel(
            name='FN124',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('siz', models.PositiveIntegerField()),
                ('sizcnt', models.PositiveIntegerField()),
                ('catch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='length_tallies', to='fn_portal.FN123')),
            ],
            options={
                'unique_together': {('catch', 'siz')},
            },
        ),
    ]
