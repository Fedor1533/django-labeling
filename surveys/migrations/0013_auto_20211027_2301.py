# Generated by Django 3.2.7 on 2021-10-27 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0012_comment_master_com'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='edit_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='edit_by',
            new_name='created_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='master_com',
        ),
        migrations.RemoveField(
            model_name='source',
            name='gen_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='surveys.source'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='master_source',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='source_class',
            field=models.CharField(blank=True, choices=[('TDE', 'TDE Source'), ('NOT TDE', 'Not TDE Source'), ('NaN', 'Unknown Source')], default='NaN', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_class',
            field=models.CharField(blank=True, choices=[('TDE', 'TDE Source'), ('NOT TDE', 'Not TDE Source'), ('NaN', 'Unknown Source')], default='NaN', max_length=20, null=True),
        ),
    ]
