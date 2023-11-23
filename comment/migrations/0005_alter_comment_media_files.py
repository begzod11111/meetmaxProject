# Generated by Django 4.2.3 on 2023-11-17 14:04

from django.db import migrations, models
import utils.managers


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_alter_comment_media_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='media_files',
            field=models.FileField(blank=True, null=True, upload_to=utils.managers.MediaPath.directory_path_datatime),
        ),
    ]
