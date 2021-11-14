# Generated by Django 3.2.7 on 2021-11-14 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0024_optsource_xray_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='optsource',
            name='gaiaedr3_dec',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='gaiaedr3_dec_error',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='gaiaedr3_ra',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='gaiaedr3_ra_error',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_dec',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_flux_w1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_flux_w2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_flux_w3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_flux_w4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_ra',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ls_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ps_decBest',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='ps_raBest',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='sdss_dec',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='optsource',
            name='sdss_ra',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='B',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='L',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='R98',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='g_d2d',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='g_gmag',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='g_nsrc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='g_s',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='s_d2d',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='s_id',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='s_otype',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='s_z',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
