# Generated by Django 3.2.7 on 2021-11-14 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0023_optcomment_optsource'),
    ]

    operations = [
        migrations.AddField(
            model_name='optsource',
            name='xray_source',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='opt_sources', to='surveys.source'),
            preserve_default=False,
        ),
    ]