# Generated by Django 3.2.7 on 2021-11-27 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0028_alter_source_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('version', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='meta_data',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='file_sources', to='surveys.metasource'),
            preserve_default=False,
        ),
    ]