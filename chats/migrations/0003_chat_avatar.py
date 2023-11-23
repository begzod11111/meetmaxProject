# Generated by Django 4.2.7 on 2023-11-20 07:48

from django.db import migrations, models
import utils.managers


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_rename_groupchat_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=utils.managers.MediaPath.directory_path_datatime),
        ),
    ]
