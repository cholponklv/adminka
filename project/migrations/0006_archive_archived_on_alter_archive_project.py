# Generated by Django 4.2.6 on 2023-10-23 10:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='archived_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='archive',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]
