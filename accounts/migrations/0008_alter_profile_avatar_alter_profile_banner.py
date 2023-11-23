# Generated by Django 4.2.7 on 2023-11-20 07:52

from django.db import migrations, models
import utils.managers


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_avatar_alter_profile_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default/avatars/avatar_default.png', upload_to=utils.managers.MediaPath.directory_path_datatime, verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='banner',
            field=models.ImageField(blank=True, default='default/banners/banner_default.jpg', upload_to=utils.managers.MediaPath.directory_path_datatime),
        ),
    ]
